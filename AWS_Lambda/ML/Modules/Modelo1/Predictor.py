from os import error
import pymongo
import pandas as pd
import json
from hyperactive import Hyperactive
from hyperactive import SimulatedAnnealingOptimizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .ClearData import ClearData
import tempfile
import boto3
import joblib
import botocore
import os

CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"
AWS_ACCESS_KEY = "AKIAVTWL6PT5PMSLZ6KP"
AWS_SECRET_KEY = "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"



class Predictor():
    

    def _get_train_data(self):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['feature-collection']
        cursor = mycol.find({'resultado': {'$ne': -1}, "serasa_info": {"$exists": True}})

        df = pd.DataFrame(list(cursor))
        new_df = df['serasa_info'].apply(lambda x: pd.Series(x))
        new_df[['cnpj','resultado']] = df[['cnpj','resultado']]

        return new_df

    def _get_predict_data(self):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['feature-collection']
        cursor = mycol.find({"$or":[{'predicao_modelo1': {"$exists": False}, "predicao_modelo1": -1}], })

        df = pd.DataFrame(list(cursor))
        new_df = df['serasa_info'].apply(lambda x: pd.Series(x))
        new_df[['cnpj','resultado']] = df[['cnpj','resultado']]

        return new_df

    def _get_feature_list(self,opt, X):
        feature_list = {}
        for key in opt.keys():
            if key in ['min_samples_split','max_depth','test_size']:
                continue
            else:
                if opt[key] is False:
                    continue
                elif opt[key] is True:
                    feature_list[key] = X[key]
                else:
                    feature = opt[key](X[key])
                    feature_list[key] = feature

        return pd.DataFrame(feature_list)

    def search_paramns(self, X, y):
        def model(opt):          
            X_new = self._get_feature_list(opt, X)
            xgb = RandomForestClassifier(
                max_depth=opt["max_depth"],
                min_samples_split = opt["min_samples_split"]
            )

            scores = cross_val_score(xgb, X_new, y, cv=7)
            score = scores.mean()
            return score

        
        features_search_space = [
            True,
            False,
            np.log1p,
            np.square,
            np.sqrt,
            np.sin,
            np.cos,
        ]

        search_space = {
            "min_samples_split": list(range(5, 55)),
            "max_depth": list(range(3, 150)),
            "test_size": [0.3, 0.28, 0.33, 0.25],
        }
        
        for c in X.columns:
            search_space[c] = features_search_space

        optimizer = SimulatedAnnealingOptimizer(
            epsilon=0.2,
            distribution="laplace",
            n_neighbours=2,
            rand_rest_p=0.01,
            p_accept=0.10,
            norm_factor="adaptive",
            annealing_rate=0.999,
            start_temp=0.85,
        )

        hyper = Hyperactive()
        hyper.add_search(model, search_space, optimizer = optimizer, n_iter=100)
        hyper.run()
        return hyper.best_para(model), hyper.best_score(model)

    def _save_opt_on_S3(self, opt, opt_filename):
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        for i in opt:
            if type(opt[i]) == type(np.log):
                opt[i] = str(opt[i]).split("'")[1]
                
        s3object = s3.Object('lambda-atf-sthima', 'models/'+opt_filename)
        s3object.put(
            Body=(bytes(json.dumps(opt).encode('UTF-8')))
        )

    def _save_model_on_S3(self, model, model_filename):
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        bucket_name = 'lambda-atf-sthima'
        location = 'models/'
        OutputFile = location + model_filename
        with tempfile.TemporaryFile() as fp:
            joblib.dump(model, fp)
            fp.seek(0)
            s3.Bucket(bucket_name).put_object(Key= OutputFile, Body=fp.read())

    def get_last_version(self, model_type = 'modelo1'):
        try:
            s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            bucket_name = 'lambda-atf-sthima'
            versions = set()
            my_bucket = s3.Bucket(bucket_name)

            for file in my_bucket.objects.all():
                if model_type in file.key and file.key.split('/')[2] != '':
                    versions.add(int(file.key.split('/')[2].split('.')[1]))

            return np.max(list(versions))
        except:
            return 0

    def _save_model_infos(self, model_name,model_version, accuracy,total_data):
        
        model_dict = {'model_name': str(model_name),
                    'model_version': int(model_version),
                    'used': False,
                    'accuracy': float(accuracy),
                    'total_data':int(total_data)}

        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['models-collection']
        mycol.insert_one(model_dict)
        return model_dict
        
    def train_new_model(self):
        df = self._get_train_data()

        ClearD = ClearData(df)
        new_df = ClearD.clear_df()  

        X = new_df.drop(columns = ['cnpj','resultado'])
        y = new_df['resultado'].astype(int)

        scaler = StandardScaler()
        X=pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        pca = PCA(n_components=5, svd_solver = 'auto')
        pca_model =pca.fit(X)

        pca_X = pd.DataFrame(pca_model.transform(X), columns = ['feature_'+str(i) for i in range(0,5)])

        opt, result_acc = self.search_paramns(pca_X, y)
        rc = RandomForestClassifier(max_depth=int(opt["max_depth"]),min_samples_split = int(opt["min_samples_split"]))

        rc.fit(self._get_feature_list(opt, pca_X), y)

        last_version = self.get_last_version('modelo1') + 1

        self._save_model_on_S3(rc,'modelo1/modelo_1.'+str(last_version)+'.sav')
        self._save_model_on_S3(pca_model,'modelo1/pca_modelo_1.'+str(last_version)+'.sav')
        self._save_opt_on_S3(opt,'modelo1/opt_modelo_1.'+str(last_version)+'.json')
        model_infos = self._save_model_infos('modelo_1',last_version, result_acc, len(pca_X))

        return model_infos

    def _download_model(self, model_name):
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        BUCKET_NAME = 'lambda-atf-sthima' 
        KEY = 'models/'+model_name
        with tempfile.TemporaryFile() as fp:
            s3.download_fileobj(Fileobj=fp, Bucket=BUCKET_NAME, Key=KEY)
            fp.seek(0)
            
            model = joblib.load(fp)

        return model

    
    def _download_opt(self, KEY):
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        bucket_name = 'lambda-atf-sthima'

        response = s3.get_object(Bucket=bucket_name, Key='models/'+KEY)
        infile = response['Body'].read().decode("utf-8")
        print(infile)
        opt = json.loads(infile)
        

        for i in opt:
            if opt[i] == 'log1p':
                opt[i] = np.log1p
            elif opt[i] == 'square':
                opt[i] = np.square
            elif opt[i] == 'sqrt':
                opt[i] = np.sqrt
            elif opt[i] == 'sin':
                opt[i] = np.sin
            elif opt[i] == 'cos':
                opt[i] = np.cos
            else:
                pass

        return opt

    def get_model_version_used(self, model_name):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['models-collection']
        cursor = mycol.find({'used':True, 'model_name':model_name})
        df = pd.DataFrame(list(cursor))
        return df['model_version'].iloc[0]
        

    def make_prediction(self, predict_df):
        version_use = self.get_model_version_used('modelo_1')
        modelo = self._download_model("modelo1/modelo_1."+str(version_use)+".sav")
        pca = self._download_model("modelo1/pca_modelo_1."+str(version_use)+".sav")
        opt = self._download_opt('modelo1/opt_modelo_1.'+str(version_use)+'.json')
        ClearD = ClearData(predict_df)
        new_predict_df = ClearD.clear_df()  
        new_x = new_predict_df.drop(columns = ['cnpj','resultado'], errors = 'ignore')

        pca_X = pd.DataFrame(pca.transform(new_x), columns = ['feature_'+str(i) for i in range(0,5)])
        y_result = modelo.predict_proba(self._get_feature_list(opt, pca_X))
        new_predict_df['predicao'] = [i[0] for i in y_result]
        new_predict_df['predicao'] = new_predict_df['predicao'].apply(lambda x: round(x,4))

        def calc_classification(x):
            if x >= 0.8:
                return  "Muito Bom"
            elif x < 0.8 and x >= 0.5:
                return "Bom"
            elif x < 0.5 and x >= 0.3:
                return "Ruim"
            elif x < 0.3:
                return "Muito Ruim"
            else:
                return "Nao calculado"

        
        new_predict_df['classificacao'] = new_predict_df['predicao'].apply(calc_classification)

        
        self._save_prediction_result(new_predict_df)
        return new_predict_df
        

    def _save_prediction_result(self, df):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['feature-collection']

        for _, line in df.iterrows():

            myquery = { "cnpj": line['cnpj'] }
            newvalues = { "$set": { "predicao_modelo1": line['predicao'], "classificacao_modelo1": line["classificacao"] } }

            mycol.update_one(myquery, newvalues)