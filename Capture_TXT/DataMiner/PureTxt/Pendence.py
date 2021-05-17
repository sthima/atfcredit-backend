import pandas as pd
from .TextInterpreter import TextInterpreter
import re

class Pendence(TextInterpreter):
    def create_df(self, text, name_type):
        df = self.create_df_by_text(text, name_type)
        return name_type, df.reset_index(drop = True)

    def _capture_information(self, text):
        
        return {'DATA':text.split(' ')[0],\
                'MODALIDADE':text.split('  ')[0][11:], \
                'AVAL':re.split('  +',text)[1].split('R$')[0].strip(), \
                'VALOR': text.split('R$')[1].strip().split(' ')[0],
                'CONTRATO':text.split('R$')[1].strip().split(' ')[1],
                'ORIGEM':re.sub('  +', ' ', text.split('R$')[1].strip()).split(' ')[2]}


    def create_df_by_text(self, text,name_type = 'PEFIN'):
        aux_text = text
        index_base = aux_text.find('R451PENDENCIA:'+name_type)
        aux_text = aux_text[index_base:]

        index_base = aux_text.find('R451OCORRENCIAS MAIS RECENTES (ATE 05) ')
        aux_text = aux_text[index_base:]

        aux_text = aux_text[aux_text.find('R452')+4:]
        aux_text = aux_text[aux_text.find('R452')+4:]
        lines = []

        while True:
            try:
                index_base = aux_text.find('R451')

                if index_base <= 0:
                    break

                index_aux = aux_text[index_base+4:].find("R452") + index_base
                aux_line = aux_text[index_base+4:index_aux]

                if len(re.sub(' +','',aux_line)) < 4:
                    break

                aux_text = aux_text[index_base+4+index_aux:]
                print(aux_line)
                lines.append(self._capture_information(aux_line))
            except:
                break
            
        df = pd.DataFrame(lines)
        return df