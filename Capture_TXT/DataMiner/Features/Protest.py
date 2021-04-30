import jellyfish as jf
import pandas as pd
import numpy as np

class Protest():
    def create_feature(self, df):
        aux_df = pd.DataFrame(df['PROTESTO'])
        aux_df['DATA'] = pd.to_datetime(aux_df['DATA'], errors = 'coerce', format = '%d/%m/%Y')
        aux_df['VALOR'] = aux_df['VALOR'].apply(lambda x: x.replace('.',''))
        aux_df['VALOR'] = aux_df['VALOR'].astype(int)

        return{
            '10_TOTAL_PROTESTOS':self.total_protest(aux_df),
            '10_STD_VALOR':self.std_protest(aux_df),
            '10_MEDIA_VALOR':self.mean_protest(aux_df),
            '10_FREQUENCIA_PROTESTO':self.frequency_protest(aux_df),
        }

    def total_protest(self, df):
        try:
            return len(df)
        except:
            return np.nan
        
    def std_protest(self, df):
        try:
            return df['VALOR'].std()
        except:
            return np.nan
        
    def mean_protest(self, df):
        try:
            return df['VALOR'].mean()
        except:
            return np.nan

    def frequency_protest(self, df):
        try:
            return abs(df['DATA'].diff().mean().days)
        except:
            return np.nan