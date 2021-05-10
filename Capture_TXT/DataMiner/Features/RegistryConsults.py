from unidecode import unidecode
import jellyfish as jf
import pandas as pd
import numpy as np
import json
import os
from ..Utils import fundos_serasa 

class LastRegistryConsults():

    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['CINCO ULTIMAS CONSULTAS'])
        except:
            return {'CINCO ULTIMAS CONSULTAS': np.nan}
            
        aux_df['QTD'] = aux_df['QTD'].astype(int)
        aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')

        def search_factoring(name):
            values = fundos_serasa.apply(lambda x: jf.levenshtein_distance(x, name))
            result = values[values <= 4]
            if len(result) > 0:
                return 1
            else:
                if 'FACTORING' in name:
                    return 1
            return 0

        aux_df['IS_FACTORING'] = aux_df.apply(lambda x: search_factoring(x['EMPRESA']), axis = 1)

        return {
            '1_TOTAL_FACTORINGS': self.count_total_factoring(aux_df),
            '1_FREQUENCIA_CONSULTAS': self.frequency_last_five_consults(aux_df),
            '1_FREQUENCIA_CONSULTAS_FACTORING': self.factoring_frequency_last_five_consults(aux_df)
        }

    def count_total_factoring(self, df):
        try:
            return (df['IS_FACTORING'] * df['QTD']).sum()
        except:
            return np.nan

    def frequency_last_five_consults(self, df):
        try:
            return abs(df['DATA'].diff().mean().days)
        except:
            return np.nan

    def factoring_frequency_last_five_consults(self, df):
        try:
            aux_df = df[df['IS_FACTORING'] >0]
            return abs(aux_df['DATA'].diff().mean().days)
        except:
            return np.nan



class RegistryConsults():
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['REGISTRO DE CONSULTAS'])
        except:
            return {'REGISTRO DE CONSULTAS': np.nan}
            
        aux_df['QTD'] = aux_df['QTD'].astype(int)

        return {'2_TENDENCIA_CRESCIMENTO':self.growth_trend_consults(aux_df),
                '2_ACIMA_MEDIA':self.above_average(aux_df),
                '2_TOTAL_CONSULTAS':self.total_weighted_consults(aux_df),
                '2_TOTAL_CONSULTAS_PONDERADA':self.total_consults(aux_df),
        }

    def growth_trend_consults(self, df):
        try:
            trend_vector = df['QTD'].rolling(window=3).mean()[-3:].reset_index(drop = True)
                    
            if trend_vector[0] <= trend_vector[1] <= trend_vector[2]:
                return 1
            else: 
                return 0
        except:
            return np.nan 

    def above_average(self, df):
        try:
            rolling_avg = df['QTD'][-3:]
            mean = df['QTD'].mean()
            if len(rolling_avg[rolling_avg>= mean+0.2*mean]) > 0:
                return 1
            return 0
        except:
            return np.nan

    def total_weighted_consults(self, df):
        try:
            df['PESO'] = range(len(df), 0, -1)
            return (df['QTD'] * df['PESO']).sum()
        except:
            return np.nan

    def total_consults(self, df):
        try:
            return df['QTD'].sum()
        except:
            return np.nan
