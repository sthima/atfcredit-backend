from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Pendence(TextInterpreter):
    def create_df(self, text, name_type):
        vector_aux = text[text.find(name_type):].split('\n')
        vector_aux = np.array(vector_aux)

        table_vector = vector_aux[:np.where(vector_aux == '')[0][0]]
        
        #----------------------------------------------------------------
        total_occurrence = table_vector[1].split('=')[1].strip()
        total_value = table_vector[2].split('=')[1].strip()
        #----------------------------------------------------------------
        
        line_aux = table_vector[4:]
        line_aux = np.array(line_aux)
        line_aux = line_aux[line_aux!='']

        table_columns = ['DATA','MODALIDADE','AVAL','VALOR','CONTRATO','ORIGEM']
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
            data['VALOR'].append(value_c)


            origem_vector = line.split(value_c)[1].strip()
            aux_origem = np.array(list(origem_vector))
            x = np.array([str.isnumeric(i) for i in aux_origem])
            i, = np.where(x == True)
            try:
                i = i.max()

                data['CONTRATO'].append(origem_vector[:i+1].strip())
                data['ORIGEM'].append(origem_vector[i+1:].strip())
            except:
                data['CONTRATO'].append('')
                data['ORIGEM'].append(origem_vector)

        data_pendence = {'TOTAL DE OCORRENCIAS':[total_occurrence], 'VALOR TOTAL':[total_value]}
        pendence_df = pd.DataFrame(data_pendence)
        
        return re.sub(' +', ' ', name_type.replace('\n','')), pd.DataFrame(data)