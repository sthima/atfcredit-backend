from DataMiner import DataBaseManager
from DataMiner import TextFileManager
from Predictor.Predictor import Predictor

dbm = DataBaseManager()

def predict_all_base():
    df_predict = Predictor(dbm.get_base_to_predict()).predict()
    dbm.set_prediction(df_predict)

def predict_new_txt(text, txt_name, txt_type):
    tfm = TextFileManager(text, txt_name,txt_type)
    df_predict = Predictor(dbm.get_one(tfm.cnpj, txt_name)).predict()
    dbm.set_prediction(df_predict)

    return df_predict
    