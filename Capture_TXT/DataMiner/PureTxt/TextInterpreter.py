import pandas as pd
import numpy as np
import re

class TextInterpreter:
    def create_df(self, text:str) -> pd.DataFrame():
        """Extract the information into text and convert it into a data frame"""
        pass

    def _default_search(self, 
                        text:str,
                        table_vector:list,\
                        table_columns:list = [],\
                        split_line:int = 0,\
                        split_column:int = 0,\
                        split_space:str = '  '):
        
        table_name = table_vector[0].split('  ')[0].strip()
        
        if len(table_columns) == 0:
            table_columns = table_vector[1+int(split_column)].split('  ')
            table_columns = np.array(table_columns)
            table_columns= table_columns[table_columns!='']
            table_columns = [i.strip().replace(':','') for i in table_columns]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']
        line_aux = [np.array(re.split(split_space,i)) for i in line_aux]
        line_aux = [i[i!=''] for i in line_aux]

        return line_aux, table_columns, table_name

    def _build_df(self, line_aux, table_columns):
        data = {i:[] for i in table_columns}
        for l in line_aux:
            for j in range(len(table_columns)):
                try:
                    data[table_columns[j]].append(l[j])
                except:
                    data[table_columns[j]].append(np.nan)
        df = pd.DataFrame(data)

        return df

    def type_txt_detect(self, text, name):
        vector_aux = text[text.find(name):].split('\n')
        vector_aux = np.array(vector_aux)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]
        count = 0
        split_column = 0
        for i in table_vector:
            if 'ATUALIZACAO' in i:
                split_column = 1
            count+=i.count('|')

        if count < 4: return 0, split_column
        else: return 1, split_column
