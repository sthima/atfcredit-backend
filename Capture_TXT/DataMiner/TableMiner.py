import pandas as pd
import numpy as np
import re

from . import CleanTxt 
from . import PureTxt 

class TableMiner():

    def __init__(self, text, text_type):
        self.text_type = text_type
        self.text = text
        self.erro_tables = set()

        self.TEXT_INTERPRETER = CleanTxt    
        if text_type == 'PURO':
            self.TEXT_INTERPRETER = PureTxt    
        

# ----------------------- Methods to captures default tables ----------------------- #
    def print_error(self, name_type):
        name_type = " ".join(name_type.split())
        self.erro_tables.add(name_type) 
        print('X - ', name_type)

    def get_PEFIN_PENDENCE(self):
        name_type = 'PEFIN'
        try:
            return self.TEXT_INTERPRETER.Pendence().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
    
    def get_REFIN_PENDENCE(self):
        name_type = 'REFIN'
        try:
            return self.TEXT_INTERPRETER.Pendence().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
              
    def get_RELATIONSHIP_WITH_MARKET(self):
        name_type = 'RELACIONAMENTO COM O MERCADO'
        try:
            return self.TEXT_INTERPRETER.Relationship().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
    
    def get_RELATIONSHIP_WITH_FACTORINGS(self):
        name_type = 'RELACIONAMENTO COM -           FACTORINGS'
        try:
            return self.TEXT_INTERPRETER.Relationship().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 

    def get_CONSULTATIONS_REGISTRATIONS(self):
        try:
            try:
                return self.TEXT_INTERPRETER.RegistryConsults().create_df(self.text, 'REGISTRO DE CONSULTAS')
            except:
                return self.TEXT_INTERPRETER.RegistryConsults().create_df(self.text, 'CONSULTAS A SERASA')

        except:
            self.print_error('REGISTRO DE CONSULTAS')
            return 

    def get_LAST_FIVE_CONSULTATIONS_REGISTRATIONS(self):
        try:
            try:
                return self.TEXT_INTERPRETER.RegistryLastFiveConsults().create_df(self.text, 'REGISTRO DE CONSULTAS')
            except:
                return self.TEXT_INTERPRETER.RegistryLastFiveConsults().create_df(self.text, 'CONSULTAS A SERASA')

        except:
            self.print_error("ULTIMOS 5 REGISTRO DE CONSULTAS" )
            return 


    def get_PAYMENTS_HISTORY_IN_MARKET(self):
        name_type = 'HISTORICO DE PAGAMENTOS NO MERCADO'
        if True:#try:
            return self.TEXT_INTERPRETER.PaymentsHistoryMarket().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return 
     
        
    def get_OVERDUE_DEBT(self):
        name_type = '\nDIVIDA VENCIDA'
        try:
            return self.TEXT_INTERPRETER.OverdueDebt().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_COMMITMENTS_EVOLUTION_ASSIGNOR(self):
        name_type = 'EVOLUCAO DE COMPROMISSOS - VISAO CEDENTE'
        try:
            return self.TEXT_INTERPRETER.CommitmentsAssignor().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    


    def get_PROTEST(self):
        name_type = '\nPROTESTO'
        
        try:
            return self.TEXT_INTERPRETER.Protest().create_df(self.text, name_type)
        except:
            self.print_error(name_type)
            return    

    def get_LAWSUIT(self):
        name_type = '\nACAO JUDICIAL'
        
        try:
            return self.TEXT_INTERPRETER.Lawsuit().create_df(self.text, name_type)
        except Exception  as e:
            print(e)

            self.print_error(name_type)
            return    

    def get_BANKRUPTCY(self):
        name_type = '\nFALENCIA'
        
        try:
            return self.TEXT_INTERPRETER.Bankruptcy().create_df(self.text, name_type)
        except Exception  as e:
            self.print_error(name_type)
            return    

    # def get_PAYMENTS_HISTORY(self):
    #     name_type = 'HISTORICO DE PAGAMENTOS (QTDE DE TITULOS)'
    #     try:
    #         return self.TEXT_INTERPRETER.PaymentsHistory().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return 

        
    # def get_PAYMENTS_HISTORY_FACTORINGS(self):
    #     name_type = 'HISTORICO DE PAGAMENTOS - FACTORINGS'
    #     try:
    #         return self.TEXT_INTERPRETER.PaymentsHistoryMarket().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return 

    # def get_PAYMENTS_HISTORY_ASSIGNOR(self):
    #     name_type = 'HISTORICO DE PAGAMENTOS - VISAO CEDENTE'
    #     try:
    #         return self.TEXT_INTERPRETER.PaymentsHistoryAssignor().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return     

    # def get_COMMITMENTS_EVOLUTION(self):
    #     name_type = 'EVOLUCAO DE COMPROMISSOS NO MERCADO'
    #     try:
    #         return self.TEXT_INTERPRETER.Commitments().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return    

    # def get_COMMITMENTS_EVOLUTION_FACTORINGS(self):
    #     name_type = 'EVOLUCAO DE COMPROMISSOS - FACTORINGS'
    #     try:
    #         return self.TEXT_INTERPRETER.CommitmentsFactorings().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return    


    # def get_MARKET_BUSINESS_REFERENCES(self):
    #     name_type = 'REFERENCIAIS DE NEGOCIOS NO MERCADO'
    #     try:
    #         return self.TEXT_INTERPRETER.BuisinessReferencesMarket().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return    

    # def get_TERM_BUSINESS_REFERENCES(self):
    #     name_type = 'REFERENCIAIS DE NEGOCIOS A PRAZO - FACTORINGS'
    #     try:
    #         return self.TEXT_INTERPRETER.BuisinessReferencesTerm().create_df(self.text, name_type)
    #     except:
    #         self.print_error(name_type)
    #         return    