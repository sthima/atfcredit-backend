from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Commitments(TextInterpreter):
    def create_df(self, text, name_type):
        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        return name_type, df


class CommitmentsFactorings(TextInterpreter):
    def create_df(self, text, name_type):
        table_columns = ['MES/ANO', 'A VENCER']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,
                                                                   split_line = split_line,
                                                                   table_columns = table_columns)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        return name_type, df


class CommitmentsAssignor(TextInterpreter):

    def create_df(self, text, name_type):
        typ, split_column_aux =  self.type_txt_detect(text, name_type)

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        split_line = split_column_aux
        split_space = '  '
        split_column = 0
        
        #----------------------------Tabela tipo 1 -----------------------------------------------
        if typ: 
            split_line = 1
            split_space = '([..\|])'
            split_column = split_column_aux

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                    table_vector = table_vector,\
                                                                    split_line = split_line,\
                                                                    split_column = split_column,\
                                                                    split_space = split_space)\
                                                                        
        if typ: 
            for l in range(len(line_aux)):
                i = np.array(line_aux[l])
                aux = np.array([len(j) for j in i])
                line_aux[l] = [j.strip() for j in i[np.where(aux >= 4)]]

        #-------------------------------------------------------------------------------------------

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        name_table = re.sub(' +', ' ', name_type)
        
        return name_type, df