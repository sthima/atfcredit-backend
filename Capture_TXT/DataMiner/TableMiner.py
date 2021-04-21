import pandas as pd
import numpy as np
import re

from .TableFinder import TableFinder

from .PureTxt import *
# from .PureTxt import Pendence, Relationship, RegistryConsults, RegistryLastFiveConsults, PaymentsHistory

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
        try:
            return Relationship().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
    
    def get_RELATIONSHIP_WITH_FACTORINGS(self):
        name_type = 'RELACIONAMENTO COM -           FACTORINGS'
        try:
            return Relationship().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 

    def get_CONSULTATIONS_REGISTRATIONS(self):
        try:
            try:
                return RegistryConsults().create_df(self.text, 'REGISTRO DE CONSULTAS')
            except:
                return RegistryConsults().create_df(self.text, 'CONSULTAS A SERASA')

        except:
            self.print_error('REGISTRO DE CONSULTAS')
            return 

    def get_LAST_FIVE_CONSULTATIONS_REGISTRATIONS(self):
        try:
            try:
                return RegistryLastFiveConsults().create_df(self.text, 'REGISTRO DE CONSULTAS')
            except:
                return RegistryLastFiveConsults().create_df(self.text, 'CONSULTAS A SERASA')

        except:
            self.print_error("ULTIMOS 5 REGISTRO DE CONSULTAS" )
            return 

    def get_PAYMENTS_HISTORY(self):
        name_type = 'HISTORICO DE PAGAMENTOS (QTDE DE TITULOS)'
        try:
            return PaymentsHistory().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
        

    def get_PAYMENTS_HISTORY_IN_MARKET(self):
        name_type = 'HISTORICO DE PAGAMENTOS NO MERCADO (VALORES EM R$)'
        try:
            return PaymentsHistoryMarket().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
        
    def get_PAYMENTS_HISTORY_FACTORINGS(self):
        name_type = 'HISTORICO DE PAGAMENTOS - FACTORINGS (VALORES EM R$)'
        try:
            return PaymentsHistoryMarket().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
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