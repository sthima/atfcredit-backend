from Modules.CaptureData import VaduApi
from Modules.CutMetrics import CutMetrics
import json
import re
import pandas as pd
import numpy as np
import jellyfish as jf 
import pymongo

vadu_columns = ['Faturamento', 'Funcionarios', 'Nome', 'OpcaoTributaria', 'Porte', 'ReceitaAbertura', 'ReceitaAtividade', 'ReceitaCapitalSocial', 'ReceitaNaturezaJuridica', 'ReceitaSituacao', 'ReceitaSituacaoEspecial', 'TotalProtesto', 'UfEndereco', 'ValorProtesto']

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)

def creat_dict(dic, columns):
    new_dic = {}
    for i in columns:
        if i in dic.keys():
            new_dic[i] = dic[i]
    return new_dic

def save_vadu_infos(vadu_result):

    df_final = vadu_result
    dado_valido = False
    if len(CutMetrics.filter(df_final)) > 0 :
        dado_valido = True

    df_final = df_final.to_dict("records")[0]

    # aux_data = json.dumps(df_final.iloc[0].to_dict(),cls=CustomEncoder)
    vadu_dict = creat_dict(df_final, vadu_columns)
    new_dict = {}

    new_dict['cnpj'] =re.sub(r'[^\w\s]','',df_final['cnpj'])  
    new_dict['vadu_info'] = vadu_dict
    new_dict['dado_valido'] = dado_valido

    data_dict_1 = json.dumps(new_dict, cls=CustomEncoder)
    data_dict_final  = json.loads(data_dict_1)

    query = {'cnpj':new_dict['cnpj']}
    key = {'$set': data_dict_final}


    CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"
    myclient = pymongo.MongoClient(CONNETCION_MONGO)
    mydb = myclient["atf_score"]
    mycol = mydb['feature-collection']
    mycol.find_one_and_update(query,key,upsert=True)

    return data_dict_final


def update_cut_rules(event, context):
    CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"
    myclient = pymongo.MongoClient(CONNETCION_MONGO)
    mydb = myclient["atf_score"]
    mycol = mydb['feature-collection']
    cursor = mycol.find()
    df = pd.DataFrame(list(cursor))
    new_df = df['vadu_info'].apply(lambda x: pd.Series(x))
    new_df[['cnpj','resultado']] = df[['cnpj','resultado']]

    aux = CutMetrics.filter(new_df)

    new_df.loc[new_df['cnpj'].isin(aux['cnpj']), 'dado_valido'] = True
    new_df.loc[~new_df['cnpj'].isin(aux['cnpj']), 'dado_valido'] = False

    df_save = pd.concat([new_df[['cnpj','dado_valido']],df[['cnpj','dado_valido']].dropna()]).drop_duplicates(keep=False).reset_index(drop = True)


    for i, line in df_save.iterrows():
        query = {'cnpj':line['cnpj']}
        key = {'$set': {'dado_valido':line['dado_valido']}}
        mycol.find_one_and_update(query,key)

    return {'response':"Regras de Corte atualizadas"}


def handler(event, context):

    # if len(str(event["razao_social"])) > 0:
    #     crawler_result = VaduCrawler(event["razao_social"]).capture_data()

    #     if len(crawler_result):
    #         cn = re.sub(r'[^\w\s]','',crawler_result['cnpj'].iloc[0])
    #         vadu_result = VaduApi(cn).capture_data()

    #         real_name = vadu_result['Nome'].iloc[0]
    #         if jf.levenshtein_distance(event["razao_social"], real_name) > 4:
    #             return({'message': 'Não foi possivel capturar pela Razão Social'})
    #         else:
    #             data_dict_final = save_vadu_infos(crawler_result, vadu_result)
    #             return({"response":data_dict_final})


    cn = re.sub(r'[^\w\s]','',event["cnpj"])
    vadu_result = VaduApi(cn).capture_data()
    data_dict_final = save_vadu_infos(vadu_result)
    return({"response":data_dict_final})




# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"cnpj":"12.289.084/0001-04", "razao_social":""}'

# '', '/var/lang/lib/python38.zip', '/var/lang/lib/python3.8', '/var/lang/lib/python3.8/lib-dynload', '/root/.local/lib/python3.8/site-packages', '/var/lang/lib/python3.8/site-packages'