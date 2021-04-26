import pandas as pd
import numpy as np
import re

from .PureTxt import *

class TableMiner():

    def __init__(self, text):
        self.text = text
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

    def get_PAYMENTS_HISTORY_ASSIGNOR(self):
        name_type = 'HISTORICO DE PAGAMENTOS - VISAO CEDENTE'
        try:
            return PaymentsHistoryAssignor().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return          
        
    def get_OVERDUE_DEBT(self):
        name_type = '\nDIVIDA VENCIDA'
        try:
            return OverdueDebt().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_COMMITMENTS_EVOLUTION(self):
        name_type = 'EVOLUCAO DE COMPROMISSOS NO MERCADO (VALORES EM R$)'
        try:
            return Commitments().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_COMMITMENTS_EVOLUTION_FACTORINGS(self):
        name_type = 'EVOLUCAO DE COMPROMISSOS - FACTORINGS (VALORES EM R$)'
        try:
            return CommitmentsFactorings().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_COMMITMENTS_EVOLUTION_ASSIGNOR(self):
        name_type = 'EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE (VALORES EM R$)'
        try:
            return CommitmentsAssignor().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_MARKET_BUSINESS_REFERENCES(self):
        name_type = 'REFERENCIAIS DE NEGOCIOS NO MERCADO (VALORES EM R$)'
        try:
            return BuisinessReferencesMarket().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_TERM_BUSINESS_REFERENCES(self):
        name_type = 'REFERENCIAIS DE NEGOCIOS A PRAZO - FACTORINGS (VALORES EM R$)'
        try:
            return BuisinessReferencesTerm().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_PROTEST(self):
        name_type = '\nPROTESTO'
        
        try:
            return Protest().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_LAWSUIT(self):
        name_type = '\nACAO JUDICIAL'
        
        try:
            return Lawsuit().create_df(self.text, name_type)
        except Exception  as e:
            print(e)

            self.print_error(name_type)
            return    

    def get_BANKRUPTCY(self):
        name_type = '\nFALENCIA'
        
        try:
            return Bankruptcy().create_df(self.text, name_type)
        except Exception  as e:
            print(e)

            self.print_error(name_type)
            return    