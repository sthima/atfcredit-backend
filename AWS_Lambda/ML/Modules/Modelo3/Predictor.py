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
import tempfile
import boto3
import joblib
import botocore
import os

from ..Modelo1.ClearData import ClearData as ClearModelo1
from ..Modelo2.ClearData import ClearData as ClearModelo2

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

        new_df1 = df['serasa_info'].apply(lambda x: pd.Series(x))
        new_df1[['cnpj','resultado']] = df[['cnpj','resultado']]

        new_df2 = df['vadu_info'].apply(lambda x: pd.Series(x))
        new_df2[['cnpj','resultado']] = df[['cnpj','resultado']]

        return new_df1, new_df2

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
            if key in ['min_samples_split','max_depth','n_estimators']:
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

    def search_paramns(self, X, y, epochs_train = 500):
        def model(opt):          
            X_new = self._get_feature_list(opt, X)
            rc = RandomForestClassifier(
                n_estimators = opt["n_estimators"],
                n_jobs = -1,
                max_depth=opt["max_depth"],
                min_samples_split = opt["min_samples_split"]
            )

            scores = cross_val_score(rc, X_new, y, cv=7)
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
            "n_estimators":[100,500,700,1000,1500],
            "min_samples_split": list(range(5, 70)),
            "max_depth": list(range(3, 150)),
        }

        for c in X.columns:
            search_space[c] = features_search_space

        optimizer = SimulatedAnnealingOptimizer(
            epsilon=0.2,
            distribution="laplace",
            n_neighbours=2,
            rand_rest_p=0.01,
            p_accept=0.15,
            norm_factor="adaptive",
            annealing_rate=0.95,
            start_temp=0.85,
        )

        hyper = Hyperactive()
        hyper.add_search(model, search_space, optimizer = optimizer, n_iter=epochs_train)
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
        
    def train_new_model(self, epochs_train = 500):
        df1, df2 = self._get_train_data()

        df_serasa = ClearModelo1(df1).clear_df()
        df_vadu = ClearModelo2(df2).clear_df()

        df_final = df_vadu.merge(df_serasa)

        X = df_serasa[df_serasa['cnpj'].isin(df_final['cnpj'])].drop(columns = ['cnpj','resultado'])
        y = df_final['resultado'].astype(int)

        scaler = StandardScaler()
        X=pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        pca = PCA(n_components=4, svd_solver = 'auto')
        pca_model =pca.fit(X)

        pca_X = pd.DataFrame(pca_model.transform(X), columns = ['feature_'+str(i) for i in range(0,4)])
        final_X = pd.concat([pca_X, df_vadu.drop(columns = ['cnpj','resultado','Nome','ReceitaSituacao'])], axis = 1)

        opt, result_acc = self.search_paramns(final_X, y, epochs_train)
        rc = RandomForestClassifier(n_estimators = int(opt["n_estimators"]),\
                                    max_depth=int(opt["max_depth"]),\
                                    min_samples_split = int(opt["min_samples_split"]))

        rc.fit(self._get_feature_list(opt, final_X), y)
        
        last_version = self.get_last_version('modelo3') + 1
        self._save_model_on_S3(rc,'modelo3/modelo_3.'+str(last_version)+'.sav')
        self._save_model_on_S3(pca_model,'modelo3/pca_modelo_3.'+str(last_version)+'.sav')
        self._save_opt_on_S3(opt,'modelo3/opt_modelo_3.'+str(last_version)+'.json')
        model_infos = self._save_model_infos('modelo_3',last_version, result_acc, len(final_X))

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
        

    def make_prediction(self, df1, df2):
        version_use = self.get_model_version_used('modelo_3')
        modelo = self._download_model("modelo3/modelo_3."+str(version_use)+".sav")
        pca = self._download_model("modelo3/pca_modelo_3."+str(version_use)+".sav")
        opt = self._download_opt('modelo3/opt_modelo_3.'+str(version_use)+'.json')

        df_serasa = ClearModelo1(df1).clear_df()
        df_vadu = ClearModelo2(df2).clear_df()

        df_final = df_vadu.merge(df_serasa)

        X = df_serasa.drop(columns = ['cnpj','resultado'])
        scaler = StandardScaler()
        X=pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        pca_X = pd.DataFrame(pca.transform(X), columns = ['feature_'+str(i) for i in range(0,4)])
        final_X = pd.concat([pca_X, df_vadu.drop(columns = ['cnpj','resultado','Nome','ReceitaSituacao'])], axis = 1)

        y_result = modelo.predict_proba(self._get_feature_list(opt, final_X))

        df_final['predicao'] = [i[0] for i in y_result]
        df_final['predicao'] = df_final['predicao'].apply(lambda x: round(x,4))

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

        
        df_final['classificacao'] = df_final['predicao'].apply(calc_classification)

        
        self._save_prediction_result(df_final)
        return df_final
        

    def _save_prediction_result(self, df):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['feature-collection']

        for _, line in df.iterrows():

            myquery = { "cnpj": line['cnpj'] }
            newvalues = { "$set": { "predicao_modelo3": line['predicao'], "classificacao_modelo3": line["classificacao"] } }

            mycol.update_one(myquery, newvalues)