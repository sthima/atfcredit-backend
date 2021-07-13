import pandas as pd
from datetime import datetime
import re
import pymongo

CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"

class CutMetrics():

    def __init__(self):
        myclient = pymongo.MongoClient(CONNETCION_MONGO)
        mydb = myclient["atf_score"]
        mycol = mydb['cut-rules-collection']
        cursor = mycol.find()
        df = pd.DataFrame(list(cursor)).iloc[0]

        self.LISTA_UfEndereco = df["UfEndereco"]
        self.LISTA_ReceitaSituacao = df["ReceitaSituacao"]
        self.TEMPO_ReceitaAbertura = df["ReceitaAbertura"]
        self.LISTA_ReceitaNaturezaJuridica = df["ReceitaNaturezaJuridica"]
        self.LISTA_ReceitaSituacaoEspecial = df["ReceitaSituacaoEspecial"]
        self.VALOR_ReceitaCapitalSocial = df["ReceitaCapitalSocial"]
        self.LISTA_OpcaoTributaria = df["OpcaoTributaria"]
        self.LISTA_Porte = df["Porte"]
        self.LISTA_ReceitaAtividade = df["ReceitaAtividade"]

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
        df = aux.filter_ReceitaNaturezaJuridica(df)
        print(len(df))
        df = aux.filter_ReceitaSituacaoEspecial(df)
        print(len(df))
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
            return df[df['UfEndereco'].isin(self.LISTA_UfEndereco)].reset_index(drop = True)
        except:
            return df
        
        
    def filter_ReceitaSituacao(self, df):
        try:
            return df[df['ReceitaSituacao'].isin(self.LISTA_ReceitaSituacao)].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaAbertura(self, df):
        try:
            df['diff_date'] = pd.to_datetime(df['ReceitaAbertura']).apply(lambda x: datetime.now().date().year - x.year)
            df = df[df['diff_date'] >= self.TEMPO_ReceitaAbertura].reset_index(drop = True)
            return df.drop(columns = ['diff_date'])
        except:
            return df
        

    def filter_ReceitaNaturezaJuridica(self, df):
        try:
            return df[df['ReceitaNaturezaJuridica'].isin(self.LISTA_ReceitaNaturezaJuridica)].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaSituacaoEspecial(self, df):
        try:
            return df[(df['ReceitaSituacaoEspecial'].isnull()) |\
                    (df['ReceitaSituacaoEspecial'].isin(self.LISTA_ReceitaSituacaoEspecial))].reset_index(drop = True)
        except:
            return df


    def filter_ReceitaCapitalSocial(self, df):
        try:
            return df[df['ReceitaCapitalSocial']>=self.VALOR_ReceitaCapitalSocial].reset_index(drop = True)
        except:
            return df


    def filter_OpcaoTributaria(self, df):
        try:
            return df[~(df['OpcaoTributaria'].isin(self.LISTA_OpcaoTributaria))].reset_index(drop = True)
        except:
            return df


    def filter_Porte(self, df):
        try:
            return df[~(df['Porte'].isin(self.LISTA_Porte))].reset_index(drop = True)
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
                setor = int(re.split(r'[^\w\s]', x.strip())[0])
                for i in self.LISTA_ReceitaAtividade:
                    if setor >= CNAE_SETORES[i][0] and  setor <= CNAE_SETORES[i][1]:
                        return True
                return False
            except:
                return False
                
        df = df[df['ReceitaAtividade'].apply(check_cnae_setor)].reset_index(drop = True)
        return df