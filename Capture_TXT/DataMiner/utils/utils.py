
from unidecode import unidecode
import pandas as pd
import numpy as np
import json
import os


def import_serasa_list():
    fundos_serasa = []
    file_name = 'DataMiner/Utils/Lista de fundos na Serasa.txt'
    with open(file_name) as infile:
        for line in infile: 
            aux = line.replace('\n','').strip().upper()
            if len(aux) > 0:
                fundos_serasa.append(unidecode(aux))
                
    return pd.Series(fundos_serasa)

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


fundos_serasa = import_serasa_list()