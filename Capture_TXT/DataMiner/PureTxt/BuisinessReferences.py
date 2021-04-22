from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class BuisinessReferencesMarket(TextInterpreter):
    def create_df(self, text, name_type):
        table_columns = ['DATA', 'VALOR', 'MEDIA']
        split_space = '    '
        split_line = 2

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_columns= table_columns,\
                                                                   table_vector = table_vector,\
                                                                   split_line = split_line,\    
                                                                   split_space = split_space)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        return name_type, df


class BuisinessReferencesTerm(TextInterpreter):
    def create_df(self, text, name_type):
        table_columns = ['DATA', 'VALOR', 'MEDIA']
        split_space = '    '
        split_line = 2

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,\
                                                                   table_columns = table_columns,\
                                                                   split_line = split_line,\
                                                                   split_space = split_space)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        return name_type, df