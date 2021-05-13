import jellyfish as jf
import pandas as pd
import numpy as np

class PaymentsHistory():
    def create_feature(self, df):
        try:
            aux_df = pd.DataFrame(df['HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)'])
        except:
            return {'HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)': np.nan}

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

        '6_PRESENCA_PAGAMENTOS':self.weight_value(aux_df),
        }


    def weight_value(self, df):
        try:
            score_count = 0
            for i,j in df.iterrows():
                if not(j['8-15_QTD'] is None):
                    score_count+=0.3
                    
                if not(j['16-30_QTD'] is None):
                    score_count+=0.5
                    
                if not(j['31-60_QTD'] is None):
                    score_count+=0.7
                    
                if not(j['+60_QTD'] is None):
                    score_count+=0.9
                    
            return score_count
        except:
            return np.nan

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
            trend_vector = df[column].rolling(window=3).mean()[-3:].reset_index(drop = True)
                    
            if trend_vector[0] <= trend_vector[1] <= trend_vector[2]:
                return 1
            else: 
                return 0
        except:
            return np.nan