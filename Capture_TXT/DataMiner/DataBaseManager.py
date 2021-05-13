import pymongo
import pandas as pd

class DataBaseManager():

    def __init__(self):
        pass

    def __get_connection(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        return myclient

    def __get_mycol(self, collection):
        myclient = self.__get_connection()
        mydb = myclient["ATFCredit"]
        mycol = mydb[collection]

        return mycol
        

    def save_TXT(self, mylist, collection = "Txt_tables"):
        x = self. __get_mycol(collection).insert_many(mylist)
        # print(x.inserted_ids)

    def get_all_base(self, collection = "Txt_tables"):
        tables = self. __get_mycol(collection).find({})
        return tables
    
    def get_tables_of_CNPJ(self, cnpj, collection = "Txt_tables"):
        tables = self. __get_mycol(collection).find_one({"cnpj": str(cnpj)})
        tables.pop('_id',None)
        tables.pop('cnpj',None)

        for k in tables.keys():
            tables[k] = pd.DataFrame(tables[k]) 

        return tables