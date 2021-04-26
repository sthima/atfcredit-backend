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


        line_aux = table_vector[2+split_line:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']


        line_aux = [np.array(re.split('  ',i)) for i in line_aux]
        line_aux = [i[i!=''] for i in line_aux]

        new_lines = []
        for line in line_aux:
            new_line = []
            try:
                new_line.append(line[0].split(' ')[0])
                new_line.append(line[0].split(' ')[1])
                new_line.append(line[2].strip().split(' ')[0])
                new_line.append(line[2].strip().split(' ')[1])

                new_line.append(line[3].strip())
                if len(line) > 4:
                    new_line.append(line[4])
                else:
                    new_line.append('')

                new_lines.append(new_line)
            except:
                continue
            
        line_aux = new_lines
        df = self._build_df(line_aux, table_columns).reset_index(drop = True)

        if len(df) >= 1:
            return re.sub(' +', ' ', name_type.replace('\n','')), df
        else:
            return