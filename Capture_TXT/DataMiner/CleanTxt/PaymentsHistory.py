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

        split_line =1
        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)
        
        typ, _  = self.type_txt_detect(text, name_type)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]
        
        table_name = table_vector[0].split('  ')[0].strip()
        
        if len(table_columns) == 0:
            table_columns = table_vector[1].split('  ')
            table_columns = np.array(table_columns)
            table_columns= table_columns[table_columns!='']
            table_columns = [i.strip().replace(':','') for i in table_columns]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        if typ == 1:
            line_aux = [np.array(i.split('|')) for i in line_aux]
            line_aux = [[i.replace('-','') for i in j] for j in line_aux]
            line_aux = [[re.sub(' +', ' ', i).strip() for i in j] for j in line_aux]
            line_aux = np.array([[i for i in j[1:]] for j in line_aux])
            line_aux = [i[(i!='')] for i in line_aux]
            new_line_aux = []
            for i in line_aux:
                if len(i) <= 0:
                    new_line_aux.append(np.nan)
                    new_line_aux.append(np.nan)
                for j in i:
                    new_line_aux.append(j)

            line_aux = [new_line_aux]

            
            
        else:
            line_aux = [np.array(i.split('  ')) for i in line_aux]
            line_aux = [i[i!=''] for i in line_aux]
            if len(line_aux) > 1:
                line_aux = line_aux[1:]

        
        df = self._build_df(line_aux, table_columns).reset_index(drop = True)

        def clear_text(x):
            x = x.iloc[0]
            
            if not(pd.isna(x)):
                x = x.replace('%', '')
                numbers = x.split('A')
                numbers = [i.strip() for i in numbers]
                numbers = [i.replace(',','.') for i in numbers]
                numbers = [i.replace('MIL','') for i in numbers]
                numbers = [i.replace('MI','') for i in numbers]
                numbers = [i.strip() for i in numbers]
                numbers = [float(i) for i in numbers]
                return [numbers[0]]
            return x

        df = df.apply(clear_text, axis = 0 )  
        df = df.fillna(0)      

        assert len(df) >= 1
        
        return re.sub(' +', ' ', name_type.replace('\n','')), df

class PaymentsHistoryMarket(TextInterpreter):

    def create_df(self, text, name_type):

        table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
            '8-15_QTD','8-15_%',
            '16-30_QTD','16-30_%',
            '31-60_QTD','31-60_%',
            '+60_QTD','+60_%',
            'PMA A VISTA QTD','PMA A VISTA %','TOTAL']

        split_line =1
        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        typ, _  = self.type_txt_detect(text, name_type)

        if typ == 0:
            table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]
        else:
            table_vector = vector_aux[:np.where(vector_aux == '* PMA = PRAZO MEDIO DE ATRASO (EM DIAS)')[0][0]]

        table_name = table_vector[0].split('  ')[0].strip()

        if len(table_columns) == 0:
            table_columns = table_vector[1].split('  ')
            table_columns = np.array(table_columns)
            table_columns= table_columns[table_columns!='']
            table_columns = [i.strip().replace(':','') for i in table_columns]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        if typ == 1:
            line_aux = [np.array(i.split('|')) for i in line_aux]
            line_aux = [[i.replace('-','') for i in j] for j in line_aux]
            line_aux = [[re.sub(' +', ' ', i).strip() for i in j] for j in line_aux]
            cont = 0
            cont_aux = 0

            new_line_aux = []
            while cont+cont_aux < len(line_aux):
                new_line = []

                new_line.append(line_aux[cont_aux+cont][0])

                aux = line_aux[cont_aux+cont+1 :cont_aux+cont+8]
                aux = np.array([[i for i in j[1:]] for j in aux])
                aux = [i[(i!='')] for i in aux]

                for i in aux:
                    if len(i) <= 0:
                        new_line.append(np.nan)
                        new_line.append(np.nan)
                    for j in i:
                        new_line.append(j)

                cont += 7
                cont_aux += 1

                new_line_aux.append(new_line)
                
            line_aux = new_line_aux
            
            
        else:
            line_aux = [np.array(i.split(' ')) for i in line_aux]
            line_aux = [i[i!=''] for i in line_aux]
            if line_aux[0][0] == 'MES/ANO':
                line_aux = line_aux[1:]
        df = self._build_df(line_aux, table_columns).reset_index(drop = True)



        def clear_text(line):
            line_aux = []
        
            for x in line:
                if not(pd.isna(x)):
                    x = x.replace('%', '')
                    numbers = x.split('A')
                    
                    numbers = [i.replace(',','.') for i in numbers]
                    numbers = [i.replace('MIL','') for i in numbers]
                    numbers = [i.replace('MI','') for i in numbers]
                    numbers = [i.strip() for i in numbers]
                    numbers = np.array(numbers)
                    numbers = numbers[numbers!='']
                    numbers = [float(i) for i in numbers]
                    
                    line_aux.append(numbers[0])
                else:
                    line_aux.append(0)
                    
            return pd.Series(line_aux)
        

        if typ == 0:
            df = df.iloc[:-1]
        df.loc[:,'PONTUAL_QTD':] = df.loc[:,'PONTUAL_QTD':].apply(clear_text, axis = 0 )
        

        
        assert len(df) >= 1
        
        return re.sub(' +', ' ', name_type.replace('\n','')), df


class PaymentsHistoryAssignor(TextInterpreter):

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

        assert len(df) >= 1
        
        return re.sub(' +', ' ', name_type.replace('\n','')), df





            

