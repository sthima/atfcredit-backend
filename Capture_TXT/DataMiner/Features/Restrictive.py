import jellyfish as jf
import pandas as pd
import numpy as np

from ..Utils import fundos_serasa 


class Restrictive():
    def last_debt(self,df):
        try:
            return df.iloc[0]['MODALIDADE']
        except:
            return np.nan


    def most_present_debt(self,df):
        try:
            return df['MODALIDADE'].max()
        except:
            return np.nan


    def debt_frequency(self,df):
        try:
            return abs(df['DATA'].diff().mean().days)
        except:
            return np.nan


    def debt_value(self,df):
        try:
            return df['VALOR'].sum()
        except:
            return np.nan


    def debt_counts(self,df):
        try:
            return len(df)
        except:
            return np.nan


class REFIN(Restrictive):
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['REFIN']) 
            aux_df['VALOR'] = aux_df['VALOR'].apply(lambda x: x.replace('.','')).astype(int)
            aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')

        except:
            return {'REFIN':np.nan}


        return {'3_ULTIMA_MODALIDADE':self.last_debt(aux_df),
                '3_MODALIDADE_MAIS_PRESENTE':self.most_present_debt(aux_df),
                '3_FREQUENCIA_DEBITO':self.debt_frequency(aux_df),
                '3_VALOR_DEBITO':self.debt_value(aux_df),
                '3_QUANTIDADE_DEBITO':self.debt_counts(aux_df),
        }


class PEFIN(Restrictive):
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['PEFIN'])
            aux_df['VALOR'] = aux_df['VALOR'].apply(lambda x: x.replace('.','')).astype(int)
            aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')

        except:
            return {'PEFIN':np.nan}

        

        def search_factoring(name):
            values = fundos_serasa.apply(lambda x: jf.levenshtein_distance(x, name))
            result = values[values <= 4]
            if len(result) > 0:
                return 1
            else:
                if 'FACTORING' in name:
                    return 1
            return 0

        aux_df['IS_FACTORING'] = aux_df.apply(lambda x: search_factoring(x['ORIGEM']), axis = 1)
        return {'4_ULTIMA_MODALIDADE':self.last_debt(aux_df),
                '4_MODALIDADE_MAIS_PRESENTE':self.most_present_debt(aux_df),
                '4_FREQUENCIA_DEBITO':self.debt_frequency(aux_df),
                '4_VALOR_DEBITO':self.debt_value(aux_df),
                '4_QUANTIDADE_DEBITO':self.debt_counts(aux_df),
                '4_TOTAL_FACTORINGS_DEBITO':self.total_factoring_debt(aux_df),
        }

    def total_factoring_debt(self, df):
        try:
            return df['IS_FACTORING'].sum()
        except:
            return np.nan
            

class OverdueDebt(Restrictive):
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['DIVIDA VENCIDA'])
            aux_df['VALOR'] = aux_df['VALOR'].apply(lambda x: x.replace('.','')).astype(int)
            aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')            
            
        except:
            return {'DIVIDA VENCIDA':np.nan}



        return {'5_ULTIMA_MODALIDADE':self.last_debt(aux_df),
                '5_MODALIDADE_MAIS_PRESENTE':self.most_present_debt(aux_df),
                '5_FREQUENCIA_DEBITO':self.debt_frequency(aux_df),
                '5_VALOR_DEBITO':self.debt_value(aux_df),
                '5_QUANTIDADE_DEBITO':self.debt_counts(aux_df),
        }