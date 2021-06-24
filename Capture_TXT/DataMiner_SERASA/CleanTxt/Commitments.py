from .TextInterpreter import TextInterpreter
from ..Utils import ClearText 
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
        
        return re.sub(' +', ' ', name_type), df


class CommitmentsFactorings(TextInterpreter):
    def create_df(self, text, name_type):
        table_columns = ['MES/ANO', 'A VENCER']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, _ = self._default_search(text= text,\
                                                                   table_vector = table_vector,
                                                                   split_line = split_line,
                                                                   table_columns = table_columns)

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        
        return re.sub(' +', ' ', name_type), df


class CommitmentsAssignor(TextInterpreter):

    def create_df(self, text, name_type):
        table_columns = ['MES/ANO','VENCIDOS','A VENCER','TOTAL']

        split_line =1
        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        typ, _  = self.type_txt_detect(text, name_type)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        if len(table_columns) == 0:
            table_columns = table_vector[1].split('  ')
            table_columns = np.array(table_columns)
            table_columns= table_columns[table_columns!='']
            table_columns = [i.strip().replace(':','') for i in table_columns]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        if typ == 0:
            line_aux = [re.sub(' +', ' ', i).split(' ') for i in line_aux]
            
        else:
            new_lines = []
            
            for i in line_aux:
                try:
                    new_line = []
                    aux = i.split('|')
                    new_line.append(aux[0].split(' ')[0])
                    new_line.append(aux[1])
                    new_line.append(aux[3])
                    new_line.append(aux[5])
                    new_lines.append(new_line)
                except:
                    continue
            
            line_aux = new_lines
        

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
            
        df.loc[:,'VENCIDOS':] = df.loc[:,'VENCIDOS':].apply(ClearText.convert_text_to_float, axis = 0 )


        return re.sub(' +', ' ', name_type.replace('\n','')), df