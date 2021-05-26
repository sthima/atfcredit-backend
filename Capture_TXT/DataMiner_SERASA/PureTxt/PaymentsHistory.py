from .TextInterpreter import TextInterpreter
from ..Utils import ClearText 
import pandas as pd
import numpy as np
import re



class PaymentsHistoryMarket(TextInterpreter):
    def create_df(self, text, name_type):
        df = self.create_df_by_text(text)
        return re.sub(' +', ' ', name_type.replace('\n','')), df.reset_index(drop = True)
   

    def _capture_information(self, text):

        def get_aux_values(aux, name, is_end = False):
            def check_is_not_line(s):
                regexp = re.compile(r'[a-z,A-Z]')
                if regexp.search(s) and len(re.findall("[0-9]", s)) <= 3:
                    return True
                return False

            aux_i = np.where(aux == name)[0][0]

            aux_f = len(aux) - aux_i

            if not(is_end):
                aux_f = np.where(aux[aux_i:] == 'HISTORICO DE PAGAMENTOS')[0][0]

            aux_ = aux[aux_i:aux_i+aux_f] 
            j = 0
            if check_is_not_line(aux_[1]):
                j = 1
            try:
                return [aux_[1+j].split('|')[1].strip(), aux_[3+j] +' '+ aux_[4+j]]

            except:
                return [aux_[1+j].split('|')[1].strip(), np.nan]
        
        aux = re.split('  +',text)
        aux= np.array([i.replace('R451','') for i in aux])

        return {'MES/ANO':aux[4], 
                'PONTUAL_QTD':get_aux_values(aux, 'PONTUAL')[0],
                'PONTUAL_%': get_aux_values(aux, 'PONTUAL')[1],
                '8-15_QTD':get_aux_values(aux, '8-15')[0],
                '8-15_%':get_aux_values(aux, '8-15')[1],
                '16-30_QTD':get_aux_values(aux, '16-30')[0],
                '16-30_%':get_aux_values(aux, '16-30')[1],
                '31-60_QTD':get_aux_values(aux, '31-60')[0],
                '31-60_%':get_aux_values(aux, '31-60')[1],
                '+60_QTD':get_aux_values(aux, '+60')[0],
                '+60_%':get_aux_values(aux, '+60')[1],
                'A_VISTA_QTD':get_aux_values(aux, 'A VISTA')[0],
                'A_VISTA_%':get_aux_values(aux, 'A VISTA')[1],
                'TOTAL':get_aux_values(aux, 'TOTAL MES', is_end = True)[0]}


    def create_df_by_text(self, text):
        def check_is_not_data(s):
            if len(re.findall(r'[a-z,A-Z]', s)) <= 3  and len(re.findall("[0-9]", s)) <= 2:
                return False
            return True
            
        aux_text = text
        index_base = aux_text.find('R451HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)')
        aux_text = aux_text[index_base:]

        aux_text = aux_text[aux_text.find('R452')+4:]
        aux_text = aux_text[aux_text.find('R452')+4:]

        lines = []

        while True:

            index_base = aux_text.find('R451')
            
            if index_base <= 0:
                break
                

            index_aux = aux_text[index_base+4:].find("R451TOTAL MES") + index_base
            index_aux = aux_text[index_aux:].find('HISTORICO DE PAGAMENTOS') + index_aux       
            
            aux_line = aux_text[index_base+4:index_aux]

            aux_text = aux_text[index_aux:].strip()

            if len(aux_line) <= 1:
                break
                
            try:
                new_line = self._capture_information(aux_line)
                if check_is_not_data(new_line['MES/ANO']):
                    break
                lines.append(new_line)
            except:
                continue


        df = pd.DataFrame(lines)
        df.loc[:,'PONTUAL_QTD':] = df.loc[:,'PONTUAL_QTD':].apply(ClearText.convert_text_to_float, axis = 0 )
        return df