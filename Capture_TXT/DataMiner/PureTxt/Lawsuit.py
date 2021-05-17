from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Lawsuit(TextInterpreter):
    def create_df(self, text):
        df = self.create_df_by_text(text)
        return 'ACAO JUDICIAL', df.reset_index(drop = True)


    def _capture_information(self, text):
        
        aux_text = re.split('  +',text)

        j = 0
        aval = np.nan
        if len(aux_text) >= 10:
            j = 1
            aval = aux_text[1]

        return {'DATA':aux_text[0].split(' ')[0],\
                'NATUREZA':aux_text[0].split(' ')[1],\
                'AVAL':aval,\
                'VALOR':aux_text[2+j],\
                'DIST':aux_text[3+j],\
                'VARA':aux_text[4+j],\
                'CIDADE':aux_text[5+j],\
                'UF':aux_text[6+j]}


    def create_df_by_text(self, text):
        aux_text = text
        index_base = aux_text.find('R451ACAO JUDICIAL')
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

                if aux_line.find('TOTAL') > 0:
                    break

                aux_text = aux_text[index_base+4+index_aux:]
                lines.append(self._capture_information(aux_line))
            except:
                break
            
        df = pd.DataFrame(lines)
        return df
    
