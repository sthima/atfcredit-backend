from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class Protest(TextInterpreter):
    def create_df(self, text):

        return 'PROTESTO', self.create_df_by_text(text)

    def _capture_information(self, text):
        
        aux_text = re.split('  +',text)

        return {'DATA':aux_text[0],\
                'VALOR':aux_text[2],\
                'CARTORIO':aux_text[3],\
                'CIDADE':aux_text[4],\
                'UF':aux_text[5]}

    def create_df_by_text(self, text):
        aux_text = text
        index_base = aux_text.find('R451PROTESTO')
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
