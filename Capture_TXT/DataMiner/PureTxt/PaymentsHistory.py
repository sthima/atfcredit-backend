from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class PaymentsHistory(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns= ['PONTUAL_QTD','PONTUAL_%',
                    '8-15_QTD','8-15_%',
                    '16-30_QTD','16-30_%',
                    '31-60_QTD','31-60_%',
                    '+60_QTD','+60_%',
                    'A VISTA_QTD']
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
        
        return name_type, df

class PaymentsHistoryMarket(TextInterpreter):
    def create_df(self, text, name_type):

        table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
                    '8-15_QTD','8-15_%',
                    '16-30_QTD','16-30_%',
                    '31-60_QTD','31-60_%',
                    '+60_QTD','+60_%',
                    'PMA A VISTA QTD','PMA A VISTA %','TOTAL']
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
        
        return name_type, df