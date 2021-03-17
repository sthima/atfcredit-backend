import pandas as pd
import numpy as np
import re

class TableFinder():

    def __init__(self, text):
        self.text = text

    def type_txt_detect(self, name):
        vector_aux = self.text[self.text.find(name):].split('\n')
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

    def __default_search(self, 
                        table_vector:list,\
                        table_columns:list = [],\
                        split_line:int = 0,\
                        split_column:int = 0,\
                        split_space:str = '  '):
        
        table_name = table_vector[0].split('  ')[0].strip()
        
        if len(table_columns) == 0:
            print(type(split_column), ' - ', split_column)
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

    def __create_df(self, line_aux, table_columns):
        data = {i:[] for i in table_columns}
        for l in line_aux:
            for j in range(len(table_columns)):
                try:
                    data[table_columns[j]].append(l[j])
                except:
                    data[table_columns[j]].append(np.nan)
        df = pd.DataFrame(data)

        return df

    def search_debt_table(self, 
                    name:str = '\nDIVIDA VENCIDA',\
                    table_columns:list = [],\
                    split_line:int = 0,\
                    split_column:int = 0,\
                    split_space:str = '  ',\
                    print_table:bool = False)-> (str, pd.DataFrame):

        vector_aux = self.text[self.text.find(name):].split('\n')
        vector_aux = np.array(vector_aux)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][1]]

        line_aux, table_columns, table_name = self.__default_search(table_vector = table_vector,\
                                                                    table_columns = table_columns,\
                                                                    split_line = split_line,\
                                                                    split_column = split_column,\
                                                                    split_space = split_space)\
                                                                    
        for i in range(len(line_aux)):
            try:
                line_aux[i] = line_aux[i][[0,1,3,4,5,6]]
            except:
                pass

        df = self.__create_df(line_aux, table_columns)
        if len(df) >= 1:
            return re.sub(' +', ' ', name.replace('\n','')), df.iloc[:-2].reset_index(drop = True)
        else:
            return

    def search_evolution_table(self, 
                    name:str,\
                    table_columns:list = [],\
                    split_line:int = 0,\
                    split_column:int = 0,\
                    split_space:str = '  ',\
                    print_table:bool = False)-> (str, pd.DataFrame):

        vector_aux = self.text[self.text.find(name):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self.__default_search(table_vector = table_vector,\
                                                                    table_columns = table_columns,\
                                                                    split_line = split_line,\
                                                                    split_column = split_column,\
                                                                    split_space = split_space)\
                                                                    

        for l in range(len(line_aux)):
            i = np.array(line_aux[l])
            aux = np.array([len(j) for j in i])
            line_aux[l] = [j.strip() for j in i[np.where(aux >= 4)]]

        df = self.__create_df(line_aux, table_columns)
        if print_table:
            print(table_name)
            display(df)
        
        return re.sub(' +', ' ', name), df.reset_index(drop = True)

    def search_default_table(self, 
                    name:str,\
                    table_columns:list = [],\
                    split_line:int = 0,\
                    split_column:int = 0,\
                    split_space:str = '  ',\
                    print_table:bool = False) -> (str, pd.DataFrame):

        """
        search_default_table: This method is used to capture any table inside the pure 
        text file of Serasa
            name: This string refers to the name of the table within the text 
            file that the method should look for

            table_columns: A list with the name of the columns of this table, 
            the method makes a standard search of the name of the columns, however it is not able to capture tables with columns of two levels

            split_line: The number of lines that must be skipped to start capturing the information

            split_space: The string used to separate the data in the text file

            print_table: Boolean that tells whether the method should print the table when capturing

        return: A tuple with the name of table and the table represents by pd.DataFrame 
        """ 

        vector_aux = self.text[self.text.find(name):].split('\n')
        vector_aux = np.array(vector_aux)
        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]

        line_aux, table_columns, table_name = self.__default_search(table_vector = table_vector,\
                                                                    table_columns = table_columns,\
                                                                    split_line = split_line,\
                                                                    split_column = split_column,\
                                                                    split_space = split_space)

        df = self.__create_df(line_aux, table_columns)
        if print_table:
            print(table_name)
            display(df)
        
        return re.sub(' +', ' ', name), df.reset_index(drop = True)

    def search_payments_table(self,
                    name:str,\
                    table_columns:list = [],\
                    split_line:int = 0,\
                    split_column:int = 0,\
                    split_space:str = '  ',\
                    print_table:bool = False):

        def clear_str(name):
            if name.count('-') >= 1 or len(name.strip()) <= 1:
                return np.nan
            return name

        vector_aux = self.text[self.text.find(name):]
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

        return name, df

    def search_pendence_table(self, name_type):
        vector_aux = self.text[self.text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]
        
        #----------------------------------------------------------------
        total_occurrence = table_vector[1].split('=')[1].strip()
        total_value = table_vector[2].split('=')[1].strip()
        #----------------------------------------------------------------
        
        line_aux = table_vector[4:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        table_columns = line_aux[0].split('   ')
        table_columns = np.array(table_columns)
        table_columns= table_columns[table_columns!='']
        table_columns = [i.strip().replace(':','') for i in table_columns]
        
        line_aux = line_aux[1:]
        
        data = {i:[] for i in table_columns}


        for line in line_aux:
            line_1 = re.sub(' +', ' ', line)
            line_1 = line_1.split(' ')

            line_2 = np.array(line.split('  '))
            line_2 = line_2[line_2!='']

            data['DATA'].append(line_1[0])
            data['MODALIDADE'].append(' '.join(line_2[0].split(' ')[1:]))
            data['AVAL'].append(line_2[1].strip().split(' ')[0])
            value_c = line.split('R$')[1].strip().split(' ')[0]
            data['VALOR CONTRATO'].append(value_c)


            origem_vector = line.split(value_c)[1].strip()
            aux_origem = np.array(list(origem_vector))
            x = np.array([str.isnumeric(i) for i in aux_origem])
            i, = np.where(x == True)
            i = i.max()

            data['ORIGEM'].append(origem_vector[:i+1].strip())
            data['LOCAL'].append(origem_vector[i+1:].strip())
        
        return total_occurrence, total_value, pd.DataFrame(data)