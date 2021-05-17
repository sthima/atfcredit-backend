import pandas as pd
from .TextInterpreter import TextInterpreter
from ..Utils import ClearText 

class CommitmentsAssignor(TextInterpreter):
    def create_df(self, text):
        df = self.create_df_by_text(text)
        return 'EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE', df.reset_index(drop = True)

    def _capture_information(self, aux_text):
        date = aux_text[4:9]

        index_base = aux_text.find("|")
        index_aux = aux_text[index_base+1:].find("|")
        vencido = aux_text[index_base:index_base+index_aux]
        vencido = vencido.replace('|', '').strip()

        aux_text = aux_text[index_base+index_aux+6:]
        index_aux = aux_text.find("|")
        vencer = aux_text[:index_aux].strip()
        
        index_base = aux_text.find("|")
        index_aux = aux_text[index_base+1:].find("  ")
        aux_text = aux_text[index_base:index_base+index_aux]
        total = aux_text.split('|')[2]

        return {'MES/ANO':date,\
                'VENCIDOS':vencido, \
                'A VENCER':vencer, \
                'TOTAL': total}


    def create_df_by_text(self, text):
        aux_text = text
        index_base = aux_text.find('R451EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)')
        aux_text = aux_text[index_base:]

        index_base = aux_text.find('R451MES/ANO  VENCIDOS                A VENCER                TOTAL')
        aux_text = aux_text[index_base+66:]

        lines = []

        while True:
            index_base = aux_text.find('R451')

            if index_base <= 0:
                break

            index_aux = aux_text[index_base+4:].find("R452")

            aux_line = aux_text[index_base:index_base+index_aux]

            if aux_line.find('TOTAL') > 0:
                break

            aux_text = aux_text[index_base+index_aux:]
            lines.append(self._capture_information(aux_line))
            
        df = pd.DataFrame(lines)
        df.loc[:,'VENCIDOS':] = df.loc[:,'VENCIDOS':].apply(ClearText.convert_text_to_float, axis = 0 )

        return df