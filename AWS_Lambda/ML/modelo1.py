from Modules.Modelo1.Predictor import Predictor
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
        new_df = df['serasa_info'].apply(lambda x: pd.Series(x))
        new_df[['cnpj','resultado']] = df[['cnpj','resultado']]
        result = Predictor().make_prediction(df)
        return {"resultado": result['resultado'].iloc[0]}
    else:
        return {"message": "CNPJ não encontrado na base"}

def predict_all_base(event, context):
    myclient = pymongo.MongoClient(CONNETCION_MONGO)
    mydb = myclient["atf_score"]
    mycol = mydb['feature-collection']
    cursor = mycol.find({})
    df = pd.DataFrame(list(cursor))
    result = Predictor().make_prediction(df)

    return {"resultado": result['resultado']}

# docker tag modelo1:latest 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo1/train:latest
        
# docker push 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo1/train:latest

# aws ecr get-login-password | docker login --username AWS --password-stdin 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo1/train:latest