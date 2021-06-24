import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from typing import Callable
import numpy as np
import re
import json
import pandas as pd
import time 
import jellyfish as jf


class VaduApi():
    def __init__(self, cnpj: Callable[[], str]):
        if type(cnpj) == type([]):
            self.cnpj = [re.sub(r'[^\w\s]','',i) for i in cnpj]

        else:
            self.cnpj = [re.sub(r'[^\w\s]','',cnpj)]


    def capture_data(self):
        url = "https://www.vadu.com.br/vadu.dll/ServicoAnaliseOperacao/Consulta/{}"
        api_columns = ['CnpjCpf', 'Nome', 'UfEndereco','ReceitaSituacao','ReceitaAbertura','ReceitaNaturezaJuridica','ReceitaSituacaoEspecial','ReceitaCapitalSocial','OpcaoTributaria','Porte','ReceitaAtividade']

        payload={}
        headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJWYWR1IiwidXNyIjoyMTQ3LCJlbWwiOiJtb3RvcnJAYXRmLmNvbS5iciIsImVtcCI6NDMzMjQxMjR9.el5_-O9x8vdlS6H7BohRBU8-sVKXza175AtaFxyn4aU',
        'Cookie': 'VADUSESSIONID=%7BA54437F5-47D0-407D-B833-4C833E773817%7D; _QRW=2043350735'
        }

        result = []
        i = 1

        for c in self.cnpj:
            
            print(i, '-> ', c)
            i+=1
            try:
                response = requests.request("POST", url.format(c), headers=headers, data=payload)
                if response.status_code  == 200:
                    result.append(json.loads(response.text))
                else:
                    print('X-', c)
            except:
                print('X-', c)

        self.df_final = pd.DataFrame(result)
        self.df_final = self.df_final[api_columns]
        return self.df_final

class VaduCrawler():
    def __init__(self, cnpj: Callable[[], str]):
        self.USUARIO = "daniel@sthima.com.br"
        self.SENHA = "Score@123"
        self.TEMPO_ATT_PROTESTO = 3
        self.NUMBER_OF_TRY = 3
        self.VADU_SITE_HOST = "https://www.vadu.com.br/vadu.dll/Autenticacao/Entrar"


        if type(cnpj) == type([]):
            self.cnpj = [re.sub(r'[^\w\s]','',i) for i in cnpj]
        else:
            self.cnpj = [re.sub(r'[^\w\s]','',cnpj)]


    def capture_data(self):
        result = self.fill_info_vector(self.cnpj , 0, [])
        df_final = pd.DataFrame() 
        for i in result:
            df_final = df_final.append(pd.DataFrame([i]), ignore_index = True)
        
        if 0 in df_final.columns:
            self.df_final = df_final.drop(index = df_final[df_final[0].notnull()].index, columns = [0]).reset_index(drop = True)
        else:
            self.df_final = df_final

        return self.df_final


    def open_vadu_web_site(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.VADU_SITE_HOST)
        return driver

        
        
    def close_modal(self):
        close_button = self.driver.find_elements_by_id("naoRedirecionaInfoCredit")
        if len(close_button):
            try:
                close_button[0].click()
            except:
                pass

    def make_login(self):
        user_input = self.driver.find_element_by_name('Codigo')
        key_input = self.driver.find_element_by_name('Senha')
        
        user_input.clear()
        user_input.send_keys(self.USUARIO)
        
        key_input.clear()
        key_input.send_keys(self.SENHA)
        
        self.driver.find_element_by_css_selector("button.btn").click()

    def login(self):      
        self.driver.get(self.VADU_SITE_HOST)
        if len(self.driver.find_elements_by_class_name('g-recaptcha-outer')):
            self.driver.close()
            
            # aux_driver = webdriver.Firefox()
            # aux_driver.get(self.VADU_SITE_HOST)
            # self.make_login(aux_driver)
            # self.close_modal(aux_driver)
            # aux_driver.close()
            print('FAÇA O LOGIN DE FORMA MANUAL')
            input()

            self.driver = self.open_vadu_web_site()
        
        self.make_login()


    def search_cnpj(self, cnpj):
        cnpj_input = self.driver.find_element_by_name('q')
        try:
            cnpj_input.clear()
        except:
            pass
        cnpj_input.send_keys(cnpj)
        cnpj_input.send_keys(Keys.ENTER)

    def necessary_update(self):
        last_update = self.driver.find_element_by_class_name('fonte-atualizacao.protestosConsultaDe').text.strip()
        
        def separet_number_and_letters(s):
            numbers = []
            text = []

            for i in s:
                try:
                    float(i)
                    numbers.append(i)
                except:
                    text.append(i)
                    
            try:
                number = float(''.join(numbers))
            except:
                number = 0

            return number, ''.join(text)
        
        time1, time2 = separet_number_and_letters(last_update)
        
        if 'mes' in time2 and time1 >= self.TEMPO_ATT_PROTESTO:
            return True
        elif 'ano' in time2:
            return True
        elif 'não consultado' in time2:
            return True
        else:
            return False


    def wait_load(self, delay = 60):
        try:
            start = time.time()
            while self.driver.find_element_by_class_name('totalProtestos').text == '' or (time.time() - start) > delay:
                self.driver.find_element_by_xpath('//a[@href="#tabProtestos"]').click()
                if self.driver.find_element_by_class_name('totalProtestos').text == '?':
                    break

            return True
        except TimeoutException:
            return False
        
    def wait_load_button(self, delay = 60):
        try:
            element = WebDriverWait(self.driver,delay).until(EC.element_to_be_clickable((By.ID, "btnAcaoAtualizarProtestoV2")))
            return True
        except TimeoutException:
            return False

    def DEFAULT_OBJ(self, cnpj,faturamento = None,\
                               funcionarios = None,\
                               total_protesto = None,\
                               valor_protesto = None):

            return {'cnpj':cnpj,
                'Faturamento':faturamento,
                'Funcionarios':funcionarios,
                'TotalProtesto':total_protesto,
                'ValorProtesto':valor_protesto}

    def creat_possibles_names_df(self):
        cnpjs=[]
        nomes=[]

        tables=self.driver.find_elements_by_xpath('//*[@id="tableCadastro"]/tbody/tr')
        for table in tables:
            aux = table.find_elements_by_xpath("./td")
            cnpjs.append(aux[0])
            nomes.append(aux[1].text)
            
        return pd.DataFrame({'cnpjs':cnpjs, 'nomes':nomes})

    def select_best_name(self, cnpj):
        possiveis_cnpjs = self.creat_possibles_names_df()
        possiveis_cnpjs['nomes'] = possiveis_cnpjs['nomes'].apply(lambda x: re.sub(' +', ' ',re.sub(r'[^\w\s]','',x)).strip())
        possiveis_cnpjs['dist_cnpj'] = possiveis_cnpjs['nomes'].apply(lambda x: jf.levenshtein_distance(x, cnpj)) 
        possiveis_cnpjs = possiveis_cnpjs.sort_values('dist_cnpj').reset_index(drop = True)
        possiveis_cnpjs['cnpjs'].iloc[0].click()
        
    def capture_VADU_info(self, cnpj):
        self.driver.get(self.VADU_SITE_HOST)
        self.login()
        self.close_modal()

        self.search_cnpj(cnpj)
        

        if len(self.driver.find_elements_by_xpath('//*[@id="tableCadastro"]/tbody/tr')):
            self.select_best_name(cnpj)
        
        result_search = self.driver.find_elements_by_id('ResultadoBusca')
        if len(result_search):
            if result_search.text == 'Pesquisa sem resultados':
                print('DEU ERRO 1')
                return self.DEFAULT_OBJ(cnpj)
            
        cnpj = self.driver.find_element_by_id('cnpjBlocoDinamico').text
        faturamento = self.driver.find_element_by_id('valorFaturamentoEstimado').text
        funcionarios = self.driver.find_element_by_id('valorQuantidadeFuncionarios').text
        
        protest_button = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#tabProtestos"]')))
        protest_button.click()

        if not(self.wait_load()):
            print('DEMOROU DMAIS')
            return self.DEFAULT_OBJ(cnpj)
        
        if self.necessary_update():
            self.driver.find_element_by_id('btnAcaoAtualizarProtestoV2').click()
            if not(self.wait_load_button()):
                print('DEU ERRO 2')
                return self.DEFAULT_OBJ(cnpj)
        
        total_protesto = self.driver.find_element_by_class_name('totalProtestos').text
        valor_protesto = self.driver.find_element_by_class_name('valor-total-protestos').text.replace('R$','').strip()
        self.driver.close()
        
        return self.DEFAULT_OBJ(cnpj,faturamento,funcionarios,total_protesto,valor_protesto)


    def fill_info_vector(self, cnpj_vector, i, vadu_infos, n_try = 0 ):
        if i >= len(cnpj_vector):
            return vadu_infos
        else:
            self.driver = self.open_vadu_web_site()
            try:
                vadu_infos.append(self.capture_VADU_info(cnpj_vector[i]))
                return self.fill_info_vector( cnpj_vector, i+1, vadu_infos)
            except Exception as e:
                print(str(e))
                try:
                    self.driver.close()
                except:
                    pass
                n_try += 1
                if n_try >= self.NUMBER_OF_TRY:
                    vadu_infos.append(cnpj_vector[i])
                    return self.fill_info_vector( cnpj_vector, i+1, vadu_infos)
                else:
                    return self.fill_info_vector( cnpj_vector, i, vadu_infos, n_try)


        
