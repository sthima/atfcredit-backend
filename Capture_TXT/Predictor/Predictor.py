import pickle as pk
import pandas as pd
import joblib
from .ClearData import ClearData

from hyperactive import Hyperactive
from hyperactive import SimulatedAnnealingOptimizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score

from sklearn.decomposition import PCA

class Predictor():
    def search_paramns(self, X, y):

        def model(opt):          
            xgb = RandomForestClassifier(
                max_depth=opt["max_depth"],
            )
            
            X_train, X_test, y_train, y_test = train_test_split(X, y,\
                                                                test_size=opt["test_size"], \
                                                                random_state=opt['random_state'])
            xgb.fit(X_train, y_train)
            y_result = xgb.predict(X_test)

            return precision_score(y_test, y_result, average='weighted')


        search_space_rf = {
            "max_depth": list(range(3, 55)),
            "test_size": [0.3, 0.28, 0.33, 0.25],
            "random_state": list(range(0, 5000)),
        }

        optimizer = SimulatedAnnealingOptimizer(
            epsilon=0.2,
            distribution="laplace",
            n_neighbours=2,
            rand_rest_p=0.001,
            p_accept=0.10,
            norm_factor="adaptive",
            annealing_rate=0.999,
            start_temp=0.9,
        )

        hyper = Hyperactive()
        hyper.add_search(model, search_space_rf,optimizer=optimizer, n_iter=5000)
        hyper.run()
        return hyper.best_para(model), hyper.best_score(model)



class SerasaPredictor(Predictor):
    def __init__(self):
        self.columns_to_use = ['7_POSSUI_CRESCIMENTO', '7_TEND_CRESCIMENTO_TOTAL',
                                '7_TOTAL_COMMITMENTS', '7_TEND_CRESCIMENTO_VENCIDOS',
                                '7_TEND_CRESCIMENTO_A_VENCER', '7_VALOR_TOTAL_VENCIDOS',
                                '7_VALOR_TOTAL_A_VENCER', '7_VALOR_TOTAL_TOTAL',
                                '6_PAGAMENTO_PERCENT_A_VISTA', '6_PAGAMENTO_PERCENT_15',
                                '4_VALOR_DEBITO', '4_ULTIMA_MODALIDADE',
                                '4_MODALIDADE_MAIS_PRESENTE', '6_PAGAMENTO_PERCENT_30',
                                '6_PAGAMENTO_VALOR_30', '10_TOTAL_PROTESTOS',
                                '5_QUANTIDADE_DEBITO', '10_MEDIA_VALOR',
                                '10_FREQUENCIA_PROTESTO', '5_MODALIDADE_MAIS_PRESENTE',
                                '5_ULTIMA_MODALIDADE', '5_VALOR_DEBITO',
                                '10_STD_VALOR', '3_VALOR_DEBITO',
                                '3_ULTIMA_MODALIDADE', '3_MODALIDADE_MAIS_PRESENTE']

    def predict(self, df):
        self.ClearD = ClearData(df)
        self.df = self.ClearD.clear_df()  
        modelo = joblib.load("Predictor/Models/RandomForest_SERASA.joblib")
        pca = pk.load(open("Predictor/Models/pca.pkl",'rb'))
        
        df_to_predict = pd.DataFrame(pca.transform(self.df.drop(columns = self.ClearD.COLUMNS_TO_DROP)))
        aux_pred = modelo.predict_proba(df_to_predict)
        self.df['prediction'] = [i[1] for i in aux_pred]

        return self.df

    def train(self, df):
        self.ClearD = ClearData(df)
        self.df = self.ClearD.clear_df()  
        y = df['result']
        self.df = self.df.drop(columns = self.ClearD.COLUMNS_TO_DROP)
        X = self.df
        self.df['result'] = y

        pca = PCA(n_components=5, svd_solver = 'auto')
        pca_model =pca.fit(self.df)
        pk.dump(pca_model, open("Predictor/Models/pca.pkl","wb"))

        best_para, best_score = self.search_paramns(X, y)

        rfc = RandomForestClassifier(
            max_depth=best_para['max_depth'],
        )

        rfc.fit(X, y)
        joblib.dump(rfc, "Predictor/Models/RandomForest_SERASA.joblib")

        return best_score




