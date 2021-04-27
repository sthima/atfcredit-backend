import pandas as pd

class TextInterpreter:
    def create_df_by_text(self, text:str) -> pd.DataFrame():
        """Extract the information into text and convert it into a data frame"""
        pass

    def __default_search(self, 
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