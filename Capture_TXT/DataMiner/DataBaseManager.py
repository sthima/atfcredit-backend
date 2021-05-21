import pymongo
import pandas as pd

class DataBaseManager():

    def __init__(self):
        pass

    def __get_mycol(self, collection):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ATFCredit"]
        mycol = mydb[collection]

        return mycol        

    def save_TXT(self, mylist, collection = "Txt_tables"):
        self. __get_mycol(collection).insert_many(mylist)

    def get_all_base(self, collection = "Txt_tables"):
        tables = self. __get_mycol(collection).find({})
        return tables

    def get_base_to_train(self, collection = "Txt_features"):
        cursor = self.__get_mycol(collection).find({'result': {'$ne': -1}})
        return pd.DataFrame(list(cursor))
    
    def get_base_to_predict(self, collection = "Txt_features"):
        cursor = self.__get_mycol(collection).find({'result': -1})
        return pd.DataFrame(list(cursor))
    
    def get_one(self, cnpj, txt_name, collection = "Txt_features"):
        cursor = self.__get_mycol(collection).find({'cnpj': cnpj, 'txt_file': txt_name})
        return pd.DataFrame(list(cursor)).iloc[:1]

    def set_prediction(self, df, collection = 'Txt_features'):
        for _,j in df.iterrows():
            myquery = { "txt_file": j['txt_file'] }
            newvalues = { "$set": { "prediction": j['prediction'] } }

            self.__get_mycol(collection).update_one(myquery, newvalues)
    