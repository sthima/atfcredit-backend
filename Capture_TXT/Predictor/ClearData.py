from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class ClearData():
    def __init__(self, df):
        self.origin_df = df
        self.MODALIDADE_COLUMNS = ['3_MODALIDADE_MAIS_PRESENTE','3_ULTIMA_MODALIDADE',
                                    '4_MODALIDADE_MAIS_PRESENTE','4_ULTIMA_MODALIDADE',
                                    '5_MODALIDADE_MAIS_PRESENTE','5_ULTIMA_MODALIDADE',
                                    '9_NATUREZA_MAIS_PRESENTE']

        self.COLUMNS_TO_DROP = ['_id','cnpj','txt_file','result','prediction']

    def _creat_all_columns(self, df):
        columns_primary = ['8_TOTAL_FALENCIA_REQ', '8_TOTAL_FALENCIA__CONC',
                    '7_TOTAL_COMMITMENTS', '7_TEND_CRESCIMENTO_VENCIDOS',
                    '7_VALOR_TOTAL_VENCIDOS', '7_TEND_CRESCIMENTO_A_VENCER',
                    '7_VALOR_TOTAL_A_VENCER', '7_TEND_CRESCIMENTO_TOTAL',
                    '7_VALOR_TOTAL_TOTAL', '7_POSSUI_CRESCIMENTO', 'ACAO JUDICIAL',
                    '6_TOTAL_PAGAMENTOS', '6_PAGAMENTO_PERCENT_15', '6_PAGAMENTO_VALOR_15',
                    '6_PAGAMENTO_TEND_CRES_15', '6_PAGAMENTO_PERCENT_30',
                    '6_PAGAMENTO_VALOR_30', '6_PAGAMENTO_TEND_CRES_30',
                    '6_PAGAMENTO_PERCENT_60', '6_PAGAMENTO_VALOR_60',
                    '6_PAGAMENTO_TEND_CRES_60', '6_PAGAMENTO_PERCENT_+60',
                    '6_PAGAMENTO_VALOR_+60', '6_PAGAMENTO_TEND_CRES_+60',
                    '6_PAGAMENTO_PERCENT_A_VISTA', '6_PAGAMENTO_VALOR_A_VISTA',
                    '6_PAGAMENTO_TEND_CRES_A_VISTA', '6_PRESENCA_PAGAMENTOS', 'PROTESTO',
                    '1_TOTAL_FACTORINGS', '1_FREQUENCIA_CONSULTAS',
                    '1_FREQUENCIA_CONSULTAS_FACTORING', '2_TENDENCIA_CRESCIMENTO',
                    '2_ACIMA_MEDIA', '2_TOTAL_CONSULTAS', '2_TOTAL_CONSULTAS_PONDERADA',
                    '2_POSSUI_CRESCIMENTO','10_TOTAL_PROTESTOS',
                    '10_STD_VALOR', '10_MEDIA_VALOR', '10_FREQUENCIA_PROTESTO',
                    '3_ULTIMA_MODALIDADE', '3_MODALIDADE_MAIS_PRESENTE',
                    '3_FREQUENCIA_DEBITO', '3_VALOR_DEBITO', '3_QUANTIDADE_DEBITO',
                    '4_ULTIMA_MODALIDADE', '4_MODALIDADE_MAIS_PRESENTE',
                    '4_FREQUENCIA_DEBITO', '4_VALOR_DEBITO', '4_QUANTIDADE_DEBITO',
                    '4_TOTAL_FACTORINGS_DEBITO', '5_ULTIMA_MODALIDADE',
                    '5_MODALIDADE_MAIS_PRESENTE', '5_FREQUENCIA_DEBITO', '5_VALOR_DEBITO',
                    '5_QUANTIDADE_DEBITO', '9_NATUREZA_MAIS_PRESENTE',
                    '9_TOTAL_ACAO_JUDICIAL', '9_VALOR_TOTAL', '9_FREQUENCIA_ACAO_JUDICIAL']

        for c in columns_primary:
            if c not in df.columns:
                df[c] = np.nan

        return df


    def clear_df(self):
        def frequency_type(x):
            try:
                if x <= 7:
                    return 1
                elif (x > 7) and (x <= 15):
                    return 2
                elif x > 15:
                    return 3
                
            except:
                return 0    

        def convert_modalidades(df, modalidade_columns):
            modalidade_columns = list(modalidade_columns)
            values = set()
            for a in modalidade_columns:
                for c in df[a].unique():
                    if type(c) == type('x'):
                        values.add(c)


            dict_str_value = {}
            j = 1
            for c in values:
                dict_str_value[c] = j
                j+=1

            
            return dict_str_value

        df = self.origin_df.copy()
        df = self._creat_all_columns(df)
        df['1_FREQUENCIA_CONSULTAS'] = df['1_FREQUENCIA_CONSULTAS'].apply(frequency_type)
        df['1_FREQUENCIA_CONSULTAS_FACTORING'] = df['1_FREQUENCIA_CONSULTAS_FACTORING'].apply(frequency_type)
        df['1_FREQUENCIA_CONSULTAS'] = df['1_FREQUENCIA_CONSULTAS'].fillna(0)
        df['1_FREQUENCIA_CONSULTAS_FACTORING'] = df['1_FREQUENCIA_CONSULTAS_FACTORING'].fillna(0)
        df['1_TOTAL_FACTORINGS'] = df['1_TOTAL_FACTORINGS'].fillna(0)

        df['2_TENDENCIA_CRESCIMENTO'] = df['2_TENDENCIA_CRESCIMENTO'].fillna(-1)
        df['2_ACIMA_MEDIA'] = df['2_ACIMA_MEDIA'].fillna(-1)
        df['2_TOTAL_CONSULTAS_PONDERADA'] = df['2_TOTAL_CONSULTAS_PONDERADA'].fillna(0)
        df['2_POSSUI_CRESCIMENTO'] = df['2_POSSUI_CRESCIMENTO'].fillna(-1)

        df['3_FREQUENCIA_DEBITO'] = df['3_FREQUENCIA_DEBITO'].apply(frequency_type)
        df['3_FREQUENCIA_DEBITO'] = df['3_FREQUENCIA_DEBITO'].fillna(0)
        df['3_VALOR_DEBITO'] = df['3_VALOR_DEBITO'].fillna(0)
        df['3_QUANTIDADE_DEBITO'] = df['3_QUANTIDADE_DEBITO'].fillna(0)

        df['4_FREQUENCIA_DEBITO'] = df['4_FREQUENCIA_DEBITO'].apply(frequency_type)
        df['4_FREQUENCIA_DEBITO'] = df['4_FREQUENCIA_DEBITO'].fillna(0)
        df['4_VALOR_DEBITO'] = df['4_VALOR_DEBITO'].fillna(0)
        df['4_QUANTIDADE_DEBITO'] = df['4_QUANTIDADE_DEBITO'].fillna(0)
        df['4_TOTAL_FACTORINGS_DEBITO'] = df['4_TOTAL_FACTORINGS_DEBITO'].fillna(0)

        df['5_FREQUENCIA_DEBITO'] = df['5_FREQUENCIA_DEBITO'].apply(frequency_type)
        df['5_FREQUENCIA_DEBITO'] = df['5_FREQUENCIA_DEBITO'].fillna(0)
        df['5_VALOR_DEBITO'] = df['5_VALOR_DEBITO'].fillna(0)
        df['5_QUANTIDADE_DEBITO'] = df['5_QUANTIDADE_DEBITO'].fillna(0)

        df['6_PAGAMENTO_PERCENT_+60'] = df['6_PAGAMENTO_PERCENT_+60'].fillna(0)
        df['6_PAGAMENTO_PERCENT_15'] = df['6_PAGAMENTO_PERCENT_15'].fillna(0)
        df['6_PAGAMENTO_PERCENT_30'] = df['6_PAGAMENTO_PERCENT_30'].fillna(0)
        df['6_PAGAMENTO_PERCENT_60'] = df['6_PAGAMENTO_PERCENT_60'].fillna(0)
        df['6_PAGAMENTO_PERCENT_A_VISTA'] = df['6_PAGAMENTO_PERCENT_A_VISTA'].fillna(0)
        df['6_PAGAMENTO_VALOR_+60'] = df['6_PAGAMENTO_VALOR_+60'].fillna(0)
        df['6_PAGAMENTO_VALOR_15'] = df['6_PAGAMENTO_VALOR_15'].fillna(0)
        df['6_PAGAMENTO_VALOR_30'] = df['6_PAGAMENTO_VALOR_30'].fillna(0)
        df['6_PAGAMENTO_VALOR_60'] = df['6_PAGAMENTO_VALOR_60'].fillna(0)
        df['6_PAGAMENTO_VALOR_A_VISTA'] = df['6_PAGAMENTO_VALOR_A_VISTA'].fillna(0)
        df['6_TOTAL_PAGAMENTOS'] = df['6_TOTAL_PAGAMENTOS'].fillna(0)
        df['6_PAGAMENTO_TEND_CRES_+60'] = df['6_PAGAMENTO_TEND_CRES_+60'].fillna(0)
        df['6_PAGAMENTO_TEND_CRES_15'] = df['6_PAGAMENTO_TEND_CRES_15'].fillna(0)
        df['6_PAGAMENTO_TEND_CRES_30'] = df['6_PAGAMENTO_TEND_CRES_30'].fillna(0)
        df['6_PAGAMENTO_TEND_CRES_60'] = df['6_PAGAMENTO_TEND_CRES_60'].fillna(0)
        df['6_PAGAMENTO_TEND_CRES_A_VISTA'] = df['6_PAGAMENTO_TEND_CRES_A_VISTA'].fillna(0)
        df['6_PRESENCA_PAGAMENTOS'] = df['6_PRESENCA_PAGAMENTOS'].fillna(0)

        df['7_TEND_CRESCIMENTO_A_VENCER'] = df['7_TEND_CRESCIMENTO_A_VENCER'].fillna(-1)
        df['7_TEND_CRESCIMENTO_TOTAL'] = df['7_TEND_CRESCIMENTO_TOTAL'].fillna(-1)
        df['7_TEND_CRESCIMENTO_VENCIDOS'] = df['7_TEND_CRESCIMENTO_VENCIDOS'].fillna(-1)
        df['7_TOTAL_COMMITMENTS'] = df['7_TOTAL_COMMITMENTS'].fillna(0)
        df['7_VALOR_TOTAL_A_VENCER'] = df['7_VALOR_TOTAL_A_VENCER'].fillna(0)
        df['7_VALOR_TOTAL_VENCIDOS'] = df['7_VALOR_TOTAL_VENCIDOS'].fillna(0)
        df['7_VALOR_TOTAL_TOTAL'] = df['7_VALOR_TOTAL_TOTAL'].fillna(0)
        df['7_POSSUI_CRESCIMENTO'] = df['7_POSSUI_CRESCIMENTO'].fillna(0)
              
        df.loc[df['8_TOTAL_FALENCIA_REQ'] > 0, '8_TOTAL_FALENCIA_REQ'] = 1
        df.loc[df['8_TOTAL_FALENCIA__CONC'] > 0, '8_TOTAL_FALENCIA__CONC'] = 1
        df['8_TOTAL_FALENCIA_REQ'] = df['8_TOTAL_FALENCIA_REQ'].fillna(0)
        df['8_TOTAL_FALENCIA__CONC'] = df['8_TOTAL_FALENCIA__CONC'].fillna(0)

        df['9_FREQUENCIA_ACAO_JUDICIAL'] = df['9_FREQUENCIA_ACAO_JUDICIAL'].apply(frequency_type)
        df['9_FREQUENCIA_ACAO_JUDICIAL'] = df['9_FREQUENCIA_ACAO_JUDICIAL'].fillna(0)
        df['9_TOTAL_ACAO_JUDICIAL'] = df['9_TOTAL_ACAO_JUDICIAL'].fillna(0)
        df['9_VALOR_TOTAL'] = df['9_VALOR_TOTAL'].fillna(0)

        df['10_FREQUENCIA_PROTESTO'] = df['10_FREQUENCIA_PROTESTO'].apply(frequency_type)
        df['10_FREQUENCIA_PROTESTO'] = df['10_FREQUENCIA_PROTESTO'].fillna(0)
        df['10_MEDIA_VALOR'] = df['10_MEDIA_VALOR'].fillna(0)
        df['10_STD_VALOR'] = df['10_STD_VALOR'].fillna(0)
        df['10_TOTAL_PROTESTOS'] = df['10_TOTAL_PROTESTOS'].fillna(0)

        dict_modalidades = convert_modalidades(df, self.MODALIDADE_COLUMNS)
        df[self.MODALIDADE_COLUMNS] = df[self.MODALIDADE_COLUMNS].replace(dict_modalidades)
        df[self.MODALIDADE_COLUMNS] = df[self.MODALIDADE_COLUMNS].fillna(0)


        column_to_drop = ['ACAO JUDICIAL','DIVIDA VENCIDA','2_TOTAL_CONSULTAS'                                          
                        'FALENCIA','PEFIN','HISTORICO DE PAGAMENTOS NO MERCADO',       
                        'CINCO ULTIMAS CONSULTAS','PROTESTO','REFIN','REGISTRO DE CONSULTAS']

        for c in column_to_drop:
            try:
                df = df.drop(columns = c)
            except:
                pass

        df_scaled = df.copy()
        scaler = StandardScaler()

        df_scaled = df_scaled.drop(columns = self.COLUMNS_TO_DROP)
        df_scaled=pd.DataFrame(scaler.fit_transform(df_scaled), columns=df_scaled.columns)

        df_scaled[self.COLUMNS_TO_DROP] = df[self.COLUMNS_TO_DROP]

        self.df_clean = df_scaled.dropna(axis=1)

        return self.df_clean