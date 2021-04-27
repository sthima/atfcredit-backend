import pandas as pd
from .TextInterpreter import TextInterpreter

class R302(TextInterpreter):
    def _capture_information(self, line):
        list_factoring_names = ['RNX', 'OPINIAO S/A', 'FIDC']
        line = line.replace('R302','')

        date = pd.to_datetime(line[:8], format = "%Y%m%d")
        name = line[8:]
        
        factoring_bool = False
        for factoring_name in list_factoring_names:
            if factoring_name in name:
                factoring_bool = True
                break
        
        return {'date':date,\
                'name':name, \
                'is_factoring':factoring_bool}


    def create_df_by_text(self, text):
        aux_text = text
        lines = []

        while True:
            index_base = aux_text.find('R302')

            if index_base <= 0:
                break

            index_aux = aux_text[index_base:].find('000')

            aux_line = aux_text[index_base:index_base+index_aux]
            aux_text = aux_text[index_base+index_aux:]
            
            lines.append(self._capture_information(aux_line))
            
        return pd.DataFrame(lines)