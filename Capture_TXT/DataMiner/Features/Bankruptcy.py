import jellyfish as jf
import pandas as pd
import numpy as np

class Bankruptcy():
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['FALENCIA'])
        except:
            return {'FALENCIA': np.nan}

        return {'8_TOTAL_FALENCIA_REQ': self.bankruptcy_type_count(aux_df, 'REQ'),
                '8_TOTAL_FALENCIA__CONC': self.bankruptcy_type_count(aux_df, 'CONC')
        }

    def bankruptcy_type_count(self, df, tipo = 'REQ'):
        try:
            df[tipo] = 0
            df.loc[df['TIPO'].str.contains(tipo), tipo] = 1
            
            return df[tipo].sum()
        except:
            return np.nan