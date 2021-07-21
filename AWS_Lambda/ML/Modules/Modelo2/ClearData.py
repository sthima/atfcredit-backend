from os import error
import pandas as pd
import numpy as np
from datetime import datetime


class ClearData():
    def __init__(self, df):
        self.df = df

    def clear_df(self):
        df = self.df
        

        df = self._ajusta_nomes()
        # def convert_number(x):
        #     try:
        #         return float(x.replace('.','').replace(',','.'))
        #     except:
        #         return np.nan

        # df['ValorProtesto'] = df['ValorProtesto'].apply(convert_number)

        df['ReceitaAbertura'] = pd.to_datetime(df['ReceitaAbertura']).apply(lambda x: datetime.now().date().year - x.year)
        df['ReceitaAbertura'] = df['ReceitaAbertura'].fillna(-1)
        df['ReceitaAbertura'] = df['ReceitaAbertura'].astype(int)

        # df['ValorProtesto'] = df['ValorProtesto'].fillna(0)

        # df['TotalProtesto'] = df['TotalProtesto'].replace('?', -1)
        # df['TotalProtesto'] = df['TotalProtesto'].replace('-', np.nan)
        # df['TotalProtesto'] = df['TotalProtesto'].fillna(-1)

        # df['TotalProtesto'] = df['TotalProtesto'].astype(int)

        df['ReceitaAtividade'] = df['ReceitaAtividade'].fillna(0)
        df['ReceitaCapitalSocial'] = df['ReceitaCapitalSocial'].fillna(0)
        df = df.drop(columns = ['OpcaoTributaria', 0 , 'ValorProtesto','TotalProtesto','Faturamento','Funcionarios'], errors = 'ignore')
    

        return df.dropna().reset_index(drop = True)

    def _ajusta_nomes(self):
        df = self.df
        
        # df['Faturamento'] = df['Faturamento'].fillna(0)
        # df['Faturamento'] = df['Faturamento'].astype(str).replace( { 'de 0 até 81.000':1,
        #                                             'de 81.000 até 360.000':2, 
        #                                             'de 360.000 até 1.500.000':3,
        #                                             'de 1.500.000 até 4.800.000':4,
        #                                             'de 4.800.000 até 10.000.000':5,
        #                                             'de 10.000.000 até 30.000.000':6, 
        #                                             'de 30.000.000 até 100.000.000':7, 
        #                                             'de 100.000.000 até 300.000.000':8,
        #                                             'de 300.000.000 até 500.000.000':9, 
        #                                             'de 500.000.000 até 1.000.000.000':10,
        #                                             'acima de 1.000.000.000':11 })
        # df['Faturamento'] = df['Faturamento'].astype(float)


        # df['Funcionarios'] = df['Funcionarios'].fillna(0)
        # df['Funcionarios'] = df['Funcionarios'].astype(str).replace( { 'de 0 até 5':1,
        #                                             'de 5 até 10':2, 
        #                                             'de 10 até 50':3, 
        #                                             'de 50 até 100':4,
        #                                             'de 100 até 500':5,
        #                                             'acima de 500':6})
        # df['Funcionarios'] = df['Funcionarios'].astype(float)


        df['UfEndereco'] = df['UfEndereco'].fillna(0)
        uif_dict = {'EX': 1, 'RJ': 2, 'PR': 3, 'SE': 4, 'PA': 5, 
                                    'MA': 6, 'CE': 7, 'SC': 8, 'AP': 9, 'DF': 10, 
                                    'PE': 11, 'AL': 12, 'RO': 13, 'RS': 14, 'MS': 15, 
                                    'SP': 16, 'RN': 17, 'PI': 18, 'MT': 19, 'ES': 20, 
                                    'RR': 21, 'AM': 22, 'MG': 23, 'BA': 24, 'GO': 25, 
                                    'PB': 26}
        df['UfEndereco'] =df['UfEndereco'].astype(str).replace(uif_dict)
        df.loc[~df['UfEndereco'].isin(list(uif_dict.keys())), 'UfEndereco'] = 0                                    
        df['UfEndereco'] = df['UfEndereco'].astype(float)


        df['ReceitaNaturezaJuridica'] = df['ReceitaNaturezaJuridica'].fillna(0)
        def convert_receita_juridica(x):
            try:
                return float(str(x).split(' ')[0].replace('-',''))
            except:
                return 0

        df['ReceitaNaturezaJuridica'] = df['ReceitaNaturezaJuridica'].apply(convert_receita_juridica)
        df['ReceitaNaturezaJuridica'] = df['ReceitaNaturezaJuridica'].astype(float)


        
        df['Porte'] = df['Porte'].fillna(0)
        df['Porte'] = df['Porte'].astype(str).replace({'EPP': 1, 'DEMAIS': 2, 'ME': 3})
        df['Porte'] = df['Porte'].astype(float)

        df.loc[~df['ReceitaSituacaoEspecial'].isin(['RECUPERACAO JUDICIAL','LIQUIDACAO EXTRA-JUDICIAL','FALIDO']), 'ReceitaSituacaoEspecial'] = 0
        df['ReceitaSituacaoEspecial'] = df['ReceitaSituacaoEspecial'].fillna(0)
        df['ReceitaSituacaoEspecial'] = df['ReceitaSituacaoEspecial'].astype(str).replace({'RECUPERACAO JUDICIAL': 1, 
                                                                            'LIQUIDACAO EXTRA-JUDICIAL': 2, 
                                                                            'FALIDO': 3,
                                                                            '':0})        
        df['ReceitaSituacaoEspecial'] = df['ReceitaSituacaoEspecial'].astype(float)

        def convert_receita_atividade(x):
            try:
                return float(str(x).split('-')[0])
            except:
                return 0

        df['ReceitaAtividade'] = df['ReceitaAtividade'].apply(convert_receita_atividade)


        return df
