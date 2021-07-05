import pandas as pd
from datetime import datetime
import re


LISTA_UfEndereco = ['RS', 'SC', 'PR', 'SP', 'RJ', 'MG']
LISTA_ReceitaSituacao = ['ATIVA']
TEMPO_ReceitaAbertura = 3
LISTA_ReceitaNaturezaJuridica = ['203-8 - Sociedade de Economia Mista', '204-6 - Sociedade Anônima Aberta', '205-4 - Sociedade Anônima Fechada', '206-2 - Sociedade Empresária Limitada', '208-9 - Sociedade Empresária em Comandita Simples', '209-7 - Sociedade Empresária em Comandita por Ações', '230-5 - Empresa Individual de Responsabilidade Limitada (de Natureza Empresária)', '231-3 - Empresa Individual de Responsabilidade Limitada (de Natureza Simples)']
LISTA_ReceitaSituacaoEspecial = ['RECUPERACAO JUDICIAL']
VALOR_ReceitaCapitalSocial = 10000
LISTA_OpcaoTributaria = ['SIMEI','SIMPLES NACIONAL']
LISTA_Porte = ['MEI','ME']
LISTA_ReceitaAtividade = ['K', 'M', 'O', 'U']

class CutMetrics():

    def __init__(self):
        pass

    @staticmethod
    def filter(df):
        aux = CutMetrics()

        print(len(df))
        df = aux.filter_UfEndereco(df)
        print(len(df))
        df = aux.filter_ReceitaSituacao(df)
        print(len(df))
        df = aux.filter_ReceitaAbertura(df)
        print(len(df))
        # df = aux.filter_ReceitaNaturezaJuridica(df)
        # print(len(df))
        # df = aux.filter_ReceitaSituacaoEspecial(df)
        # print(len(df))
        df = aux.filter_ReceitaCapitalSocial(df)
        print(len(df))
        # df = aux.filter_OpcaoTributaria(df)
        df = aux.filter_Porte(df)
        print(len(df))
        df = aux.filter_ReceitaAtividade(df)
        print(len(df))
        
        return df
    
    def filter_UfEndereco(self, df):
        try:
            return df[df['UfEndereco'].isin(LISTA_UfEndereco)].reset_index(drop = True)
        except:
            return df
        
        
    def filter_ReceitaSituacao(self, df):
        try:
            return df[df['ReceitaSituacao'].isin(LISTA_ReceitaSituacao)].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaAbertura(self, df):
        try:
            df['diff_date'] = pd.to_datetime(df['ReceitaAbertura']).apply(lambda x: datetime.now().date().year - x.year)
            df = df[df['diff_date'] >= TEMPO_ReceitaAbertura].reset_index(drop = True)
            return df.drop(columns = ['diff_date'])
        except:
            return df
        

    def filter_ReceitaNaturezaJuridica(self, df):
        try:
            return df[df['ReceitaNaturezaJuridica'].isin(LISTA_ReceitaNaturezaJuridica)].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaSituacaoEspecial(self, df):
        try:
            return df[(df['ReceitaSituacaoEspecial'].isnull()) |\
                    (df['ReceitaSituacaoEspecial'].isin(LISTA_ReceitaSituacaoEspecial))].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaCapitalSocial(self, df):
        try:
            return df[df['ReceitaCapitalSocial']>=VALOR_ReceitaCapitalSocial].reset_index(drop = True)
        except:
            return df


    def filter_OpcaoTributaria(self, df):
        try:
            return df[~(df['OpcaoTributaria'].isin(LISTA_OpcaoTributaria))].reset_index(drop = True)
        except:
            return df


    def filter_Porte(self, df):
        try:
            return df[~(df['Porte'].isin(LISTA_Porte))].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaAtividade(self, df):
        def check_cnae_setor(x):
            CNAE_SETORES = {'A':(1,3),'B':(5,9),'C':(10,33),
                            'D':(35,35),'E':(36,39),'F':(41,43),
                            'G':(45,47),'H':(49,53),'I':(55,56),
                            'J':(58,63),'K':(64,66),'L':(68,68),
                            'M':(69,75),'N':(77,82),'O':(84,84),
                            'P':(85,85),'Q':(86,88),'R':(90,93),
                            'S':(94,96),'T':(97,97),'U':(99,99)}


            try:
                setor = int(re.split(r'[^\w\s]',x)[0])
                for i in LISTA_ReceitaAtividade:
                    if setor >= CNAE_SETORES[i][0] and  setor <= CNAE_SETORES[i][1]:
                        return False
                return True
            except:
                return True
        try:
            return df[df['ReceitaAtividade'].apply(check_cnae_setor)].reset_index(drop = True)
        except:
            return df
