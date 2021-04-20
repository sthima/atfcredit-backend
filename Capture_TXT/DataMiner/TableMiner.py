import pandas as pd
import numpy as np
import re

from .TableFinder import TableFinder

from .PureTxt import Pendence, Relationship

class TableMiner():

    def __init__(self, text):
        self.text = text
        self.tf = TableFinder(text)
        self.erro_tables = set()

# ----------------------- Methods to captures default tables ----------------------- #
    def print_error(self, name_type):
        name_type = " ".join(name_type.split())
        self.erro_tables.add(name_type) 
        print('X - ', name_type)

    def get_PEFIN_PENDENCE(self):
        name_type = 'PEFIN'
        try:
            return Pendence().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
    
    def get_REFIN_PENDENCE(self):
        name_type = 'REFIN'
        try:
            return Pendence().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
            
            
    def get_RELATIONSHIP_WITH_MARKET(self):
        name_type = 'RELACIONAMENTO COM O MERCADO'
        if True:#try:
            return Relationship().create_df(self.text, name_type)
        # except:
        #     self.print_error(name_type)
        #     return 
    
    def get_RELATIONSHIP_WITH_FACTORINGS(self):
        name_type = 'RELACIONAMENTO COM -           FACTORINGS'
        try:
            return Relationship().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 

    def get_CONSULTATIONS_REGISTRATIONS(self, last_fives = False):
        try:
            table_columns = ['MES_1', 'QTD_1', 'MES_2', 'QTD_2', 'CINCO_ULTIMAS_CONSULTAS', 'QTD']
            try:
                name_table, df = self.tf.search_default_table('REGISTRO DE CONSULTAS', table_columns = table_columns, split_line = 1)
            except:
                name_table, df = self.tf.search_default_table('CONSULTAS A SERASA', table_columns = table_columns, split_line = 1)

            if not(last_fives):
                df_1_aux = df[['MES_1', 'QTD_1']]
                df_1_aux.columns = ['MES','QTD']
                df_2_aux = df[['MES_2', 'QTD_2']]
                df_2_aux.columns = ['MES','QTD']

                df_1 = pd.concat([df_1_aux,df_2_aux])
                return 'REGISTRO DE CONSULTAS', df_1.reset_index(drop = True)

            else:
                df_2 = df[['CINCO_ULTIMAS_CONSULTAS', 'QTD']].iloc[:-1]
                def extract_date(line):
                    aux_ = line.strip().split(' ')
                    date = aux_[0]
                    name = ' '.join(aux_[1:])
                    return pd.Series({'DATA':date, 
                                    'CINCO_ULTIMAS_CONSULTAS':name.strip()})
                    
                df_2['DATA'] = '' 
                df_2[['DATA','CINCO_ULTIMAS_CONSULTAS']] = df_2['CINCO_ULTIMAS_CONSULTAS'].apply(extract_date)
                df_2.columns = ['EMPRESA', 'QTD','DATA']

                return 'CINCO ULTIMAS CONSULTAS', df_2.reset_index(drop = True)
        except:
            self.erro_tables.add('REGISTRO DE CONSULTAS') 
            print('X - REGISTRO DE CONSULTAS')
            return 

    def get_PAYMENTS_HISTORY(self):
        try:
            table_columns= ['PONTUAL_QTD','PONTUAL_%',
                    '8-15_QTD','8-15_%',
                    '16-30_QTD','16-30_%',
                    '31-60_QTD','31-60_%',
                    '+60_QTD','+60_%',
                    'A VISTA_QTD']

            return self.tf.search_default_table('HISTORICO DE PAGAMENTOS (QTDE DE TITULOS)', \
                                table_columns= table_columns, \
                                split_line =1)
        except:
            self.erro_tables.add('HISTORICO DE PAGAMENTOS (QTDE DE TITULOS)') 
            print('X - HISTORICO DE PAGAMENTOS (QTDE DE TITULOS)')
            return 

    def get_PAYMENTS_HISTORY_IN_MARKET(self):
        try:
            table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
                    '8-15_QTD','8-15_%',
                    '16-30_QTD','16-30_%',
                    '31-60_QTD','31-60_%',
                    '+60_QTD','+60_%',
                    'PMA A VISTA QTD','PMA A VISTA %','TOTAL']

            return self.tf.search_default_table('HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)', \
                            table_columns = table_columns, \
                            split_line = 1, \
                            split_space = ' ')
        except:
            self.erro_tables.add('HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)') 
            print('X - HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)')
            return 

    def get_PAYMENTS_HISTORY_FACTORINGS(self):
        try:
            table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
                    '8-15_QTD','8-15_%',
                    '16-30_QTD','16-30_%',
                    '31-60_QTD','31-60_%',
                    '+60_QTD','+60_%',
                    'PMA A VISTA QTD','PMA A VISTA %','TOTAL']

            return self.tf.search_default_table('HISTORICO DE PAGAMENTOS - FACTORINGS (VALORES EM R$)', \
                            table_columns = table_columns, \
                            split_line = 1, \
                            split_space = ' ')
        except:
            self.erro_tables.add('HISTORICO DE PAGAMENTOS - FACTORINGS (VALORES EM R$)') 
            print('X - HISTORICO DE PAGAMENTOS - FACTORINGS (VALORES EM R$)')
            return 

    def get_OVERDUE_DEBT(self):
        try:
            table_columns = ['DATA','MODALIDADE','VALOR','TITULO','INST_COBRADORA','LOCAL']
            name_type = '\nDIVIDA VENCIDA'

            return self.tf.search_debt_table(name_type, \
                            table_columns = table_columns, \
                            split_line = 1, \
                            split_space = ' ')
        except:
            self.erro_tables.add('DIVIDA VENCIDA') 
            print('X -', 'DIVIDA VENCIDA')
            return 

    def get_PAYMENTS_HISTORY_ASSIGNOR(self):
        try:
            name_type = 'HISTORICO DE PAGAMENTOS - VISAO CEDENTE'
            typ, split_column =  self.tf.type_txt_detect(name_type)
            table_columns= ['MES/ANO','PONTUAL_QTD','PONTUAL_%',
                            '8-15_QTD','8-15_%',
                            '16-30_QTD','16-30_%',
                            '31-60_QTD','31-60_%',
                            '+60_QTD','+60_%',
                            'A_VISTA_QTD','A_VISTA_QTD']
            if not(split_column):
                return self.tf.search_default_table('HISTORICO DE PAGAMENTOS - VISAO CEDENTE', \
                                table_columns = table_columns, \
                                split_line = 1, \
                                split_space = ' ')
            
            else:
                return self.tf.search_payments_table('HISTORICO DE PAGAMENTOS - VISAO CEDENTE', \
                                    table_columns = table_columns, \
                                    split_space = ' ')

        except Exception as error:
            self.erro_tables.add('HISTORICO DE PAGAMENTOS - VISAO CEDENTE (VALORES EM R$ MILHARES)') 
            print('X - HISTORICO DE PAGAMENTOS - VISAO CEDENTE (VALORES EM R$ MILHARES) - ', error)
            return 

    def get_COMMITMENTS_EVOLUTION(self):
        try:
            return self.tf.search_default_table('EVOLUCAO DE COMPROMISSOS NO MERCADO (VALORES EM R$)')
        except:
            self.erro_tables.add('EVOLUCAO DE COMPROMISSOS NO MERCADO (VALORES EM R$)') 
            print('X - EVOLUCAO DE COMPROMISSOS NO MERCADO (VALORES EM R$)')
            return 

    def get_COMMITMENTS_EVOLUTION_FACTORINGS(self):
        try:
            return self.tf.search_default_table('EVOLUCAO DE COMPROMISSOS - FACTORINGS (VALORES EM R$)', \
                                split_line = 1, \
                                table_columns = ['MES/ANO', 'A VENCER'])
        except:
            self.erro_tables.add('EVOLUCAO DE COMPROMISSOS - FACTORINGS (VALORES EM R$)') 
            print('X - EVOLUCAO DE COMPROMISSOS - FACTORINGS (VALORES EM R$)')
            return 

    def get_COMMITMENTS_EVOLUTION_ASSIGNOR(self):
        try:
            name_type = 'EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)'
            typ, split_column =  self.tf.type_txt_detect(name_type)
            if typ:
                return self.tf.search_evolution_table(name_type, \
                                                    split_line = 1, \
                                                    split_column = split_column, \
                                                    split_space = '([..\|])')
            else:
                return self.tf.search_default_table(name_type, split_column = split_column, split_line = split_column)
        except Exception as error:
            self.erro_tables.add(name_type) 
            print('X - '+name_type, ' - ', error)
            return 

    def get_MARKET_BUSINESS_REFERENCES(self):
        try:
            return self.tf.search_default_table('REFERENCIAIS DE NEGOCIOS NO MERCADO (VALORES EM R$)', \
                                split_space = '    ')
        except:
            self.erro_tables.add('REFERENCIAIS DE NEGOCIOS NO MERCADO (VALORES EM R$)') 
            print('X - REFERENCIAIS DE NEGOCIOS NO MERCADO (VALORES EM R$)')
            return 

    def get_TERM_BUSINESS_REFERENCES(self):
        try:
            return self.tf.search_default_table('REFERENCIAIS DE NEGOCIOS A PRAZO - FACTORINGS (VALORES EM R$)',  \
                                split_space = '    ',  \
                                split_line = 1,  \
                                table_columns = ['DATA', 'VALOR', 'MEDIA'])
        except:
            self.erro_tables.add('REFERENCIAIS DE NEGOCIOS A PRAZO - FACTORINGS (VALORES EM R$)') 
            print('X - REFERENCIAIS DE NEGOCIOS A PRAZO - FACTORINGS (VALORES EM R$)')
            return 