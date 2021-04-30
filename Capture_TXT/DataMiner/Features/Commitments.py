import jellyfish as jf
import pandas as pd
import numpy as np

class Commitments():
    def create_feature(self, df):
        aux_df = pd.DataFrame(df['EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)'])
        return {
            '7_TOTAL_COMMITMENTS': self.count_commitments(aux_df),
            '7_TEND_CRESCIMENTO_VENCIDOS': self.growth_trend_consults(aux_df, 'VENCIDOS'),
            '7_VALOR_TOTAL_VENCIDOS': self.total_value_commitments(aux_df, 'VENCIDOS'),
            '7_TEND_CRESCIMENTO_A_VENCER': self.growth_trend_consults(aux_df, 'A VENCER'),
            '7_VALOR_TOTAL_A_VENCER': self.total_value_commitments(aux_df, 'A VENCER'),
            '7_TEND_CRESCIMENTO_TOTAL': self.growth_trend_consults(aux_df, 'TOTAL'),
            '7_VALOR_TOTAL_TOTAL': self.total_value_commitments(aux_df, 'TOTAL'),

        }




    def growth_trend_consults(self, df, column):
        rolling_avg = df[column].rolling(window=5).mean()[-3:]
        mean = df[column].mean()
        std = df[column].std()

        if len(rolling_avg[rolling_avg>= mean - std]) >= len(rolling_avg):
            return 1

        return 0

    def total_value_commitments(self, df, column):
        return df[column].sum()

    def count_commitments(self, df):
        return len(df)