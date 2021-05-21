import pickle as pk
import pandas as pd
import joblib
from .ClearData import ClearData

class Predictor():
    def __init__(self, df):
        self.ClearD = ClearData(df)
        self.df = self.ClearD.clear_df()       
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



    def predict(self):
        modelo = joblib.load("Predictor/Models/DecisionTree_2021-05-20.joblib")
        pca = pk.load(open("Predictor/Models/pca.pkl",'rb'))
        
        df_to_predict = pd.DataFrame(pca.transform(self.df.drop(columns = self.ClearD.COLUMNS_TO_DROP)))
        aux_pred = modelo.predict_proba(df_to_predict)
        self.df['prediction'] = [i[1] for i in aux_pred]

        return self.df




