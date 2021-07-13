from Modules.Modelo3.Predictor import Predictor
import pymongo
import pandas as pd

def train(event, context):
    acc = Predictor().train_new_model()
    return {"acc":acc}

CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"

def predict_cnpj(event, context):
    myclient = pymongo.MongoClient(CONNETCION_MONGO)
    mydb = myclient["atf_score"]
    mycol = mydb['feature-collection']
    cursor = mycol.find({"cnpj":event['cnpj']})
    df = pd.DataFrame(list(cursor))

    if len(df)> 0:
        if len(df[df['vadu_info'].notnull()])<= 0: 
            return {"message": "CNPJ sem informacoes do VADU"}
        elif len(df[df['serasa_info'].notnull()])<= 0: 
            return {"message": "CNPJ sem informacoes do SERASA"}  

        else:
            new_df1 = df['serasa_info'].apply(lambda x: pd.Series(x))
            new_df1[['cnpj','resultado']] = df[['cnpj','resultado']]

            new_df2 = df['vadu_info'].apply(lambda x: pd.Series(x))
            new_df2[['cnpj','resultado']] = df[['cnpj','resultado']]

            result = Predictor().make_prediction(new_df1, new_df2)
            return {"resultado": result['predicao'].iloc[0]}
            
    else:
        return {"message": "CNPJ não encontrado na base"}

# docker tag modelo3:latest 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo3:latest
        
# docker push 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo3:latest

# aws ecr get-login-password | docker login --username AWS --password-stdin 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo3:latest