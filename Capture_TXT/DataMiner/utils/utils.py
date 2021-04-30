
from unidecode import unidecode
import pandas as pd
import numpy as np
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



fundos_serasa = import_serasa_list()