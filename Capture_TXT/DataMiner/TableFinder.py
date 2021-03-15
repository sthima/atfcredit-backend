import pandas as pd
import numpy as np
import re

class TableFinder():

    def __init__(self, text):
        self.text = text

    def search_table(self, 
                    name:str,\
                    table_columns:list = [],\
                    split_line:int = 0,\
                    split_space:str = '  ',\
                    print_table:bool = False) -> (str, pd.DataFrame):

        """
        search_table: This method is used to capture any table inside the pure 
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
        
        table_name = table_vector[0].split('  ')[0].strip()
        
        if len(table_columns) == 0:
            table_columns = table_vector[1].split('  ')
            table_columns = np.array(table_columns)
            table_columns= table_columns[table_columns!='']
            table_columns = [i.strip().replace(':','') for i in table_columns]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']
        line_aux = [np.array(i.split(split_space)) for i in line_aux]
        line_aux = [i[i!=''] for i in line_aux]
        
        data = {i:[] for i in table_columns}
        for l in line_aux:
            for j in range(len(table_columns)):
                try:
                    data[table_columns[j]].append(l[j])
                except:
                    data[table_columns[j]].append(np.nan)
        df = pd.DataFrame(data)
            
        if print_table:
            print(table_name)
            display(df)
        
        return re.sub(' +', ' ', name), df.reset_index(drop = True)

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