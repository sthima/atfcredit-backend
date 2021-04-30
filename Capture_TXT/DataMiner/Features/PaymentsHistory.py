import jellyfish as jf
import pandas as pd
import numpy as np

class PaymentsHistory():
    def create_feature(self, df):

        aux_df = pd.DataFrame(df['HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)'])

        def get_value(x):
            try:
                return int(x)
            except:
                try:
                    x = str(x).split(' ')
                    for value in x :
                        try:
                            return int(value) * 1000
                        except:
                            continue
                    return np.nan
                except:
                    return np.nan

        aux_df['8-15_QTD'] = aux_df['8-15_QTD'].apply(get_value)
        aux_df['16-30_QTD'] = aux_df['16-30_QTD'].apply(get_value)
        aux_df['31-60_QTD'] = aux_df['31-60_QTD'].apply(get_value)
        aux_df['+60_QTD'] = aux_df['+60_QTD'].apply(get_value)
        aux_df['A_VISTA_QTD'] = aux_df['A_VISTA_QTD'].apply(get_value)

        return {'6_TOTAL_PAGAMENTOS':self.total_depts_count(aux_df),

        '6_PAGAMENTO_PERCENT_15':self.percent_of_debt(aux_df, '8-15_QTD'),
        '6_PAGAMENTO_VALOR_15':self.total_of_debt_value(aux_df, '8-15_QTD'),
        '6_PAGAMENTO_TEND_CRES_15':self.growth_trend_debt(aux_df, '8-15_QTD'),
        
        '6_PAGAMENTO_PERCENT_30':self.percent_of_debt(aux_df, '16-30_QTD'),
        '6_PAGAMENTO_VALOR_30':self.total_of_debt_value(aux_df, '16-30_QTD'),
        '6_PAGAMENTO_TEND_CRES_30':self.growth_trend_debt(aux_df, '16-30_QTD'),

        '6_PAGAMENTO_PERCENT_60':self.percent_of_debt(aux_df,'31-60_QTD' ),
        '6_PAGAMENTO_VALOR_60':self.total_of_debt_value(aux_df,'31-60_QTD' ),
        '6_PAGAMENTO_TEND_CRES_60':self.growth_trend_debt(aux_df, '31-60_QTD'),

        '6_PAGAMENTO_PERCENT_+60':self.percent_of_debt(aux_df, '+60_QTD'),
        '6_PAGAMENTO_VALOR_+60':self.total_of_debt_value(aux_df, '+60_QTD'),
        '6_PAGAMENTO_TEND_CRES_+60':self.growth_trend_debt(aux_df, '+60_QTD'),

        '6_PAGAMENTO_PERCENT_A_VISTA':self.percent_of_debt(aux_df,'A_VISTA_QTD'),
        '6_PAGAMENTO_VALOR_A_VISTA':self.total_of_debt_value(aux_df, 'A_VISTA_QTD'),
        '6_PAGAMENTO_TEND_CRES_A_VISTA':self.growth_trend_debt(aux_df, 'A_VISTA_QTD'),
        }




    def total_depts_count(self, df):
        try:
            return len(df)
        except:
            return np.nan

    def percent_of_debt(self, df, column):
        try:
            aux = len(df[df[column] > 0])
            return int(aux / len(df)*100)
        except:
            return np.nan

    def total_of_debt_value(self, df, column):
        try:
            return df[column].sum()
        except:
            return np.nan

    def growth_trend_debt(self, df,column):
        try:
            rolling_avg = df[column].rolling(window=3).mean()[-3:]
            mean = df[column].mean()
            std = df[column].std()

            if len(rolling_avg[rolling_avg>= mean - std]) >= len(rolling_avg):
                return 1

            return 0
        except:
            return np.nan