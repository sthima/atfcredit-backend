import jellyfish as jf
import pandas as pd
import numpy as np

class Commitments():
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)'])
        except:
            return {'EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)': np.nan}

        return {
            '7_TOTAL_COMMITMENTS': self.count_commitments(aux_df),
            '7_TEND_CRESCIMENTO_VENCIDOS': self.growth_trend_consults(aux_df, 'VENCIDOS'),
            '7_VALOR_TOTAL_VENCIDOS': self.total_value_commitments(aux_df, 'VENCIDOS'),
            '7_TEND_CRESCIMENTO_A_VENCER': self.growth_trend_consults(aux_df, 'A VENCER'),
            '7_VALOR_TOTAL_A_VENCER': self.total_value_commitments(aux_df, 'A VENCER'),
            '7_TEND_CRESCIMENTO_TOTAL': self.growth_trend_consults(aux_df, 'TOTAL'),
            '7_VALOR_TOTAL_TOTAL': self.total_value_commitments(aux_df, 'TOTAL'),
            '7_POSSUI_CRESCIMENTO': self.have_growth(aux_df),

        }


    def have_growth(self, df):
        try:
            score = 0
            for i in range(0,len(df)):
                if (df.iloc[i]['VENCIDOS'] > 0) or (df.iloc[i]['A VENCER'] > 0):
                    if i < 3:
                        score += 0.8
                    else:
                        score += 0.2

            return round(score,2)
        except:
            return 0

    def growth_trend_consults(self, df, column):
        try:
            trend_vector = df[column].rolling(window=3).mean()[-3:].reset_index(drop = True)
                    
            if trend_vector[0] <= trend_vector[1] <= trend_vector[2]:
                return 1
            else: 
                return 0
        except:
            return np.nan
            
    def total_value_commitments(self, df, column):
        try:
            return df[column].sum()
        except:
            return np.nan

    def count_commitments(self, df):
        try:
            return len(df)
        except:
            return np.nan
