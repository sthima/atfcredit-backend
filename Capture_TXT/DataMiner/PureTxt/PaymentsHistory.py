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


class PaymentsHistoryAssignor(TextInterpreter):

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


    def create_df(self, text, name_type):

        table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
                        '8-15_QTD','8-15_%',
                        '16-30_QTD','16-30_%',
                        '31-60_QTD','31-60_%',
                        '+60_QTD','+60_%',
                        'A_VISTA_QTD','A_VISTA_QTD']

        typ, split_column =  self.type_txt_detect(text, name_type)

        split_line = 0

        #----------------------------Tabela tipo 1 -----------------------------------------------
        if not(split_column):
            split_line = 1

            vector_aux = text[text.find(name_type):].split('\n')
            vector_aux = np.array(vector_aux)
            table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

            line_aux, table_columns, table_name = self._default_search(text= text,\
                                                                    table_vector = table_vector,\
                                                                    table_columns = table_columns,\
                                                                    split_line = 1,
                                                                    split_space = ' ')
            df = self._build_df(line_aux, table_columns).reset_index(drop = True)
            name_table = re.sub(' +', ' ', name_type)
        
            return name_type, df


        #--------------------------Tabela tipo 2 --------------------------------------------------
        else:
            def clear_str(name):
                if name.count('-') >= 1 or len(name.strip()) <= 1:
                    return np.nan
                return name

            vector_aux = text[text.find(name_type):]
            vector_aux = vector_aux[:vector_aux.find('*')].split('\n')
            vector_aux = np.array(vector_aux)
            vector_aux = vector_aux[4:]

            lines_split = np.where(vector_aux == '')[0]

            df = pd.DataFrame()

            for i in range(len(lines_split)):
                aux_line = vector_aux[lines_split[i]+1:lines_split[i+1]]
                if aux_line[0].count('TOTAL')>= 1:
                    break
                
                data = {}
                
                data['MES/ANO'] = aux_line[0]

                data['PONTUAL_QTD'] = clear_str(aux_line[1].split('|')[1].strip())
                data['PONTUAL_'] = clear_str(aux_line[1].split('|')[2].strip())

                data['8-15_QTD'] = clear_str(aux_line[2].split('|')[1].strip())
                data['8-15_%'] = clear_str(aux_line[2].split('|')[2].strip())

                data['16-30_QTD'] = clear_str(aux_line[3].split('|')[1].strip())
                data['16-30_%'] = clear_str(aux_line[3].split('|')[2].strip())

                data['31-60_QTD'] = clear_str(aux_line[4].split('|')[1].strip())
                data['31-60_%'] = clear_str(aux_line[4].split('|')[2].strip())

                data['+60_QTD'] = clear_str(aux_line[5].split('|')[1].strip())
                data['+60_%'] = clear_str(aux_line[5].split('|')[2].strip())

                data['A_VISTA_QTD'] = clear_str(aux_line[6].split('|')[1].strip())
                data['A_VISTA_%'] = clear_str(aux_line[6].split('|')[2].strip())
                
                df = df.append(pd.DataFrame([data]), ignore_index = True)

            return name_type, df





            

