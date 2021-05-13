from .TextInterpreter import TextInterpreter
import pandas as pd
import numpy as np
import re


class RegistryConsults(TextInterpreter):
    def create_df(self, text):

        df = self.create_df_by_text(text)

        return 'REGISTRO DE CONSULTAS', df.reset_index(drop = True)

    def _capture_information(self, line):
        
        year = line[:2]
        month = line[2:4]
        qtd = line[8:line.find("000A")]
        
        return {'MES':month+'/'+year,\
                'searches':qtd}

    def create_df_by_text(self, text):
        aux_text = text
        lines = []

        while True:
            index_base = aux_text.find('R301')

            if index_base <= 0:
                break

            index_aux = aux_text[index_base+4:].find("R301")

            aux_line = aux_text[index_base+4:index_base+index_aux]
            
            if len(aux_line.strip()) <= 0:
                break
                
            aux_text = aux_text[index_base+index_aux:]
            
            lines.append(self._capture_information(aux_line))
            
        return pd.DataFrame(lines)