from Modules.CaptureData import VaduApi, VaduCrawler
import json
import re
import pandas as pd
import numpy as np
import jellyfish as jf 

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

def handler(event, context):

    if len(str(event["razao_social"])) > 0:
        crawler_result = VaduCrawler(event["razao_social"]).capture_data()

        if len(crawler_result):
            cn = re.sub(r'[^\w\s]','',crawler_result['cnpj'].iloc[0])
            vadu_result = VaduApi(cn).capture_data()

            real_name = vadu_result['Nome'].iloc[0]
            if jf.levenshtein_distance(event["razao_social"], real_name) > 4:
                return({'message': 'Não foi possivel capturar pela Razão Social'})
            else:
                return({"response":json.dumps(pd.concat([crawler_result,vadu_result],axis = 1).iloc[0].to_dict(),cls=CustomEncoder)})
            
    if len(str(event["cnpj"])) > 0:
        crawler_result = VaduCrawler(event["cnpj"]).capture_data()
        if len(crawler_result):
            cn = re.sub(r'[^\w\s]','',crawler_result['cnpj'].iloc[0])
            vadu_result = VaduApi(cn).capture_data()
            return({"response":json.dumps(pd.concat([crawler_result,vadu_result],axis = 1).iloc[0].to_dict(),cls=CustomEncoder)})
        else:
            return({'message': 'Não foi possivel capturar pelo CNPJ'})




# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"cnpj":"12.289.084/0001-04", "razao_social":""}'

# '', '/var/lang/lib/python38.zip', '/var/lang/lib/python3.8', '/var/lang/lib/python3.8/lib-dynload', '/root/.local/lib/python3.8/site-packages', '/var/lang/lib/python3.8/site-packages'