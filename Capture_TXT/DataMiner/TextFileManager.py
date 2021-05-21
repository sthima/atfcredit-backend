import pandas as pd
import numpy as np
import json
import os
import re

from .TableMiner import TableMiner
from .FeatureManager import FeatureManager
from .DataBaseManager import DataBaseManager
from .Utils import CustomEncoder

dbm = DataBaseManager()

class TextFileManager():
    
    def __init__(self, text, file_path,txt_type, result = -1):
        self.result = result
        self.file_path = file_path
        self.text = text
        self.cnpj = self.extract_cnpj(text)
        self.tm = TableMiner(text, txt_type)
        self.create_tables_dict()
        self.create_features_by_tables()
        self.save_txt_tables()
        self.save_txt_features()
        

    def extract_cnpj(self, text):
        cpnj = text[text.find('CNPJ:'):].split('\n')[0]
        cpnj = cpnj.replace('CNPJ:','').strip()
        return re.sub('[^A-Za-z0-9]+', '',cpnj[:18])

    def create_tables_dict(self):
        tables_list = [self.tm.get_CONSULTATIONS_REGISTRATIONS(),

                        self.tm.get_LAST_FIVE_CONSULTATIONS_REGISTRATIONS(),
                        
                        self.tm.get_PAYMENTS_HISTORY_IN_MARKET(),

                        self.tm.get_COMMITMENTS_EVOLUTION_ASSIGNOR(),

                        self.tm.get_PEFIN_PENDENCE(),
                        
                        self.tm.get_REFIN_PENDENCE(),

                        self.tm.get_OVERDUE_DEBT(),

                        self.tm.get_PROTEST(),
                        self.tm.get_LAWSUIT(),
                        self.tm.get_BANKRUPTCY(),

                        ]
        tables_obj = {}

        for r in tables_list:
            if not(r is None):
                if len(r) <= 2:
                    tables_obj[r[0]] = json.loads(r[1].to_json())
                else:
                    tables_obj[r[0]] = json.loads(r[1].to_json()) 
                    tables_obj[r[2]] = json.loads(r[3].to_json()) 

        tables_obj['ERROR'] = list(self.tm.erro_tables)

        tables_obj['cnpj'] = self.cnpj
        tables_obj['txt_file'] = self.file_path
        tables_obj['result'] = int(self.result)
        
        self.tables_obj = tables_obj

        return tables_obj

    def create_features_by_tables(self):
        self.features = FeatureManager(self.tables_obj).get_features()

        self.features.update({'result': self.result,
                                'cnpj':  self.cnpj,
                                'txt_file': self.file_path,
                                'prediction': -1})

        return self.features


    def save_txt_tables(self):
        dict_to_save = self.tables_obj.copy()
        dbm.save_TXT([dict_to_save], 'Txt_tables')
        del dict_to_save

    def save_txt_features(self):
        dict_to_save = self.features.copy()
        data_dict_1 = json.dumps(self.features,cls=CustomEncoder)
        data_dict_final  = json.loads(data_dict_1)

        dbm.save_TXT([data_dict_final], 'Txt_features')
        del dict_to_save
        
    