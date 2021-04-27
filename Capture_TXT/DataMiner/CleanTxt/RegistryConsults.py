from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class RegistryConsults(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns = ['MES_1', 'QTD_1', 'MES_2', 'QTD_2', 'CINCO_ULTIMAS_CONSULTAS', 'QTD']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,\
                                                                   table_columns = table_columns,\
                                                                   split_line = split_line)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        df_1_aux = df[['MES_1', 'QTD_1']]
        df_1_aux.columns = ['MES','QTD']
        df_2_aux = df[['MES_2', 'QTD_2']]
        df_2_aux.columns = ['MES','QTD']

        df_1 = pd.concat([df_1_aux,df_2_aux])
        return 'REGISTRO DE CONSULTAS', df_1.reset_index(drop = True)



class RegistryLastFiveConsults(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns = ['MES_1', 'QTD_1', 'MES_2', 'QTD_2', 'CINCO_ULTIMAS_CONSULTAS', 'QTD']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,\
                                                                   table_columns = table_columns,\
                                                                   split_line = split_line)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        df_2 = df[['CINCO_ULTIMAS_CONSULTAS', 'QTD']].iloc[:-1]
        def extract_date(line):
            aux_ = line.strip().split(' ')
            date = aux_[0]
            name = ' '.join(aux_[1:])
            return pd.Series({'DATA':date, 
                            'CINCO_ULTIMAS_CONSULTAS':name.strip()})
            
        df_2['DATA'] = '' 
        df_2[['DATA','CINCO_ULTIMAS_CONSULTAS']] = df_2['CINCO_ULTIMAS_CONSULTAS'].apply(extract_date)
        df_2.columns = ['EMPRESA', 'QTD','DATA']

        return 'CINCO ULTIMAS CONSULTAS', df_2.reset_index(drop = True)