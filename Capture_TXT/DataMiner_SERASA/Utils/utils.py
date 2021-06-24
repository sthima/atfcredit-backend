
from unidecode import unidecode
import pandas as pd
import numpy as np
import json


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


class ClearText():
    @staticmethod
    def convert_text_to_float(line):
        line_aux = []

        for x in line:
            try:
                if not(pd.isna(x)):
                    
                    mult = 1000
                    if x.find('MIL') >= 0:
                        mult = 1000
                    elif x.find('%') >= 0:
                        mult = 1 
                    elif x.find('M') >= 0 or x.find('MI') >= 0: 
                        mult = 1000000
                    
                    x = x.replace('%', '')
                    
                    numbers = x.split('A')

                    numbers = [i.replace(',','.') for i in numbers]
                    numbers = [i.replace('MIL','') for i in numbers]
                    numbers = [i.replace('MI','') for i in numbers]
                    numbers = [i.replace('M','') for i in numbers]
                    numbers = [i.strip() for i in numbers]
                    numbers = np.array(numbers)
                    numbers = numbers[numbers!='']
                    numbers = [float(i)*mult for i in numbers]

                    line_aux.append(numbers[0])
                else:
                    line_aux.append(0)
            except:
                line_aux.append(np.nan)

        return pd.Series(line_aux)


fundos_serasa = import_serasa_list()