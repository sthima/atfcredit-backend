from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Relationship(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns = ['0-6 MESES', '6MES-1ANO', '1-3ANOS', '3-5ANOS', '5-10ANOS', '+10ANOS','INAT']


        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,\
                                                                   table_columns = table_columns)

        df = self._build_df(line_aux, table_columns)
        
        return re.sub(' +', ' ', name_type), df.reset_index(drop = True)



        