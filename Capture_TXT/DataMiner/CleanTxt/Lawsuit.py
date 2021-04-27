from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Lawsuit(TextInterpreter):
    def create_df(self, text, name_type):
        table_columns= ['DATA', 'NATUREZA', 'AVAL', 'VALOR','DIST','VARA','CIDADE', 'UF']
        split_line = 1

        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        i = np.flatnonzero(np.core.defchararray.find(vector_aux,'TOTAL DE OCORRENCIAS')!=-1)[0]
        table_vector = vector_aux[:i]

        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        line_aux = [re.sub('  +', '  ', i.replace('\n','')) for i in line_aux]
        line_aux = [np.array(re.split('  ',i)) for i in line_aux]

        new_lines = []
        for line in line_aux:
            new_line = []
            try:
                new_line.append(line[0].split(' ')[0])
                new_line.append(' '.join(line[0].split(' ')[1:]))
                
                j = 0
                if "R$" in line:           
                    if line[1] == 'R$':
                        new_line.append('')
                        new_line.append(line[2+j])
                    else:
                        new_line.append(line[1])
                        new_line.append(line[3])
                        j += 1
                else: 
                    if len(line) <= 5:
                        new_line.append('')
                        new_line.append('')
                        j = -2
                        
                    else:
                        new_line.append(line[1])
                        new_line.append('')
                        j = -1
                
                 
                new_line.append(line[3+j])
                new_line.append(line[4+j])
                new_line.append(line[5+j])
                new_line.append(line[6+j])

                new_lines.append(new_line)
            except:
                continue
            
        line_aux = new_lines
        df = self._build_df(line_aux, table_columns).reset_index(drop = True)
        if len(df) >= 1:
            return re.sub(' +', ' ', name_type.replace('\n','')), df
        else:
            return
   
