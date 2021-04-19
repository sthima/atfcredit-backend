import pandas as pd
import numpy as np
import os
from .TableMiner import TableMiner
import json

class TextFileManager():
    
    def __init__(self, file_path):
        text = ""
        with open(file_path) as infile:
            for line in infile:
                text += line

        self.text = text
        self.cnpj = self.extract_cnpj(text)
        self.tm = TableMiner(text)

    def extract_cnpj(self, text):
        cpnj = text[text.find('CNPJ:'):].split('\n')[0]
        cpnj = cpnj.replace('CNPJ:','').strip()
        return cpnj

    def create_tables_dict(self):
        tables_list = [self.tm.get_RELATIONSHIP_WITH_MARKET(),
                        self.tm.get_RELATIONSHIP_WITH_FACTORINGS(),
                        self.tm.get_CONSULTATIONS_REGISTRATIONS(),
                        self.tm.get_CONSULTATIONS_REGISTRATIONS(last_fives = True),
                        self.tm.get_PAYMENTS_HISTORY(),
                        self.tm.get_PAYMENTS_HISTORY_IN_MARKET(),
                        self.tm.get_PAYMENTS_HISTORY_FACTORINGS(),
                        self.tm.get_PAYMENTS_HISTORY_ASSIGNOR(),
                        self.tm.get_OVERDUE_DEBT(),
                        self.tm.get_COMMITMENTS_EVOLUTION(),
                        self.tm.get_COMMITMENTS_EVOLUTION_FACTORINGS(),
                        self.tm.get_COMMITMENTS_EVOLUTION_ASSIGNOR(),
                        self.tm.get_MARKET_BUSINESS_REFERENCES(),
                        self.tm.get_TERM_BUSINESS_REFERENCES(),
                        self.tm.get_PEFIN_PENDENCE(),
                        self.tm.get_REFIN_PENDENCE()]
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

        return tables_obj

