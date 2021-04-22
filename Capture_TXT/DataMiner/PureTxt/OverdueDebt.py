from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class OverdueDebt(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns= ['DATA','MODALIDADE','VALOR','TITULO','INST_COBRADORA','LOCAL']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][1]]

        line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                   table_vector = table_vector,\
                                                                   table_columns = table_columns,\
                                                                   split_line = split_line)\
                                                                    
        for i in range(len(line_aux)):
            try:
                line_aux[i] = line_aux[i][[0,1,3,4,5,6]]
            except:
                pass

        df = self._build_df(line_aux, table_columns).reset_index(drop = True)

        if len(df) >= 1:
            return re.sub(' +', ' ', name_type.replace('\n','')), df.iloc[:-2].reset_index(drop = True)
        else:
            return
        