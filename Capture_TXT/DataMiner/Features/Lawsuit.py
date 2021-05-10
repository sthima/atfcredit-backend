import jellyfish as jf
import pandas as pd
import numpy as np

class Lawsuit():
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['ACAO JUDICIAL'])
        except:
            return {'ACAO JUDICIAL': np.nan}
            
        aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')

        return {'9_NATUREZA_MAIS_PRESENTE':self.most_present_lawsuit(aux_df),
            '9_TOTAL_ACAO_JUDICIAL':self.total_lawsuit(aux_df),
            '9_VALOR_TOTAL':self.total_value(aux_df),
            '9_FREQUENCIA_ACAO_JUDICIAL':self.frequency_lawsuit(aux_df)
        }

    def most_present_lawsuit(self, df):
        try:
            return df['NATUREZA'].max()
        except:
            return np.nan 

    def total_lawsuit(self, df):
        try:
            return len(df)
        except:
            return np.nan 

    def total_value(self, df):
        try:
            try:
                df['VALOR'] = df['VALOR'].apply(lambda x: x.replace('.',''))
                return df['VALOR'].astype(int).sum()
            except:
                return 0
        except:
            return np.nan 
        
    def frequency_lawsuit(self, df):
        try:
            return abs(df['DATA'].diff().mean().days)
        except:
            return np.nan 