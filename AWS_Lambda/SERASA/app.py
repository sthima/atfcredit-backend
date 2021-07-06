from Modules.DataMiner_SERASA import TextFileManager, CustomEncoder
import json
import pymongo 
import re
import pandas as pd
import numpy as np 

serasa_columns = ['8_TOTAL_FALENCIA_REQ', '8_TOTAL_FALENCIA__CONC', '7_TOTAL_COMMITMENTS',
       '7_TEND_CRESCIMENTO_VENCIDOS', '7_VALOR_TOTAL_VENCIDOS',
       '7_TEND_CRESCIMENTO_A_VENCER', '7_VALOR_TOTAL_A_VENCER',
       '7_TEND_CRESCIMENTO_TOTAL', '7_VALOR_TOTAL_TOTAL',
       '7_POSSUI_CRESCIMENTO', 'ACAO JUDICIAL',
       'HISTORICO DE PAGAMENTOS NO MERCADO', 'PROTESTO',
       'CINCO ULTIMAS CONSULTAS', '2_TENDENCIA_CRESCIMENTO', '2_ACIMA_MEDIA',
       '2_TOTAL_CONSULTAS', '2_TOTAL_CONSULTAS_PONDERADA',
       '2_POSSUI_CRESCIMENTO', 'REFIN', 'PEFIN', 'DIVIDA VENCIDA',
       'data_consulta','6_TOTAL_PAGAMENTOS', '6_PAGAMENTO_PERCENT_15',
       '6_PAGAMENTO_VALOR_15', '6_PAGAMENTO_TEND_CRES_15',
       '6_PAGAMENTO_PERCENT_30', '6_PAGAMENTO_VALOR_30',
       '6_PAGAMENTO_TEND_CRES_30', '6_PAGAMENTO_PERCENT_60',
       '6_PAGAMENTO_VALOR_60', '6_PAGAMENTO_TEND_CRES_60',
       '6_PAGAMENTO_PERCENT_+60', '6_PAGAMENTO_VALOR_+60',
       '6_PAGAMENTO_TEND_CRES_+60', '6_PAGAMENTO_PERCENT_A_VISTA',
       '6_PAGAMENTO_VALOR_A_VISTA', '6_PAGAMENTO_TEND_CRES_A_VISTA',
       '6_PRESENCA_PAGAMENTOS', '1_TOTAL_FACTORINGS', '1_FREQUENCIA_CONSULTAS',
       '1_FREQUENCIA_CONSULTAS_FACTORING', '10_TOTAL_PROTESTOS',
       '10_STD_VALOR', '10_MEDIA_VALOR', '10_FREQUENCIA_PROTESTO',
       '9_NATUREZA_MAIS_PRESENTE', '9_TOTAL_ACAO_JUDICIAL', '9_VALOR_TOTAL',
       '9_FREQUENCIA_ACAO_JUDICIAL', '3_ULTIMA_MODALIDADE',
       '3_MODALIDADE_MAIS_PRESENTE', '3_FREQUENCIA_DEBITO', '3_VALOR_DEBITO',
       '3_QUANTIDADE_DEBITO', '4_ULTIMA_MODALIDADE',
       '4_MODALIDADE_MAIS_PRESENTE', '4_FREQUENCIA_DEBITO', '4_VALOR_DEBITO',
       '4_QUANTIDADE_DEBITO', '4_TOTAL_FACTORINGS_DEBITO',
       '5_ULTIMA_MODALIDADE', '5_MODALIDADE_MAIS_PRESENTE',
       '5_FREQUENCIA_DEBITO', '5_VALOR_DEBITO', '5_QUANTIDADE_DEBITO','REGISTRO DE CONSULTAS',
       'FALENCIA']

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)

def creat_dict(dic, columns):
    new_dic = {}
    for i in columns:
        if i in dic.keys():
            new_dic[i] = dic[i]
    return new_dic

def save_serasa_infos(df_final):
    # aux_data = json.dumps(df_final.iloc[0].to_dict(),cls=CustomEncoder)
    serasa_dict = creat_dict(df_final, serasa_columns)
    new_dict = {}

    new_dict['cnpj'] =re.sub(r'[^\w\s]','',df_final['cnpj'])  
    new_dict['serasa_info'] = serasa_dict
    new_dict['resultado'] = df_final['result']
    new_dict['predicao_modelo1'] = -1
    new_dict['predicao_modelo3'] = -1

    data_dict_1 = json.dumps(new_dict, cls=CustomEncoder)
    data_dict_final  = json.loads(data_dict_1)

    query = {'cnpj':new_dict['cnpj']}
    key = {'$set': data_dict_final}


    CONNETCION_MONGO = "mongodb+srv://atfUser:mvOX8tCv5Tv4pvJU@atfcluster.t51do.mongodb.net/test"
    myclient = pymongo.MongoClient(CONNETCION_MONGO)
    mydb = myclient["atf_score"]
    mycol = mydb['feature-collection']
    mycol.find_one_and_update(query,key,upsert=True)

    return data_dict_final

def handler(event, context):
    tfm = TextFileManager(event['text'], event['txt_type'], event['result'])
    save_serasa_infos(tfm.features)
    return {"features":json.dumps(tfm.features, cls=CustomEncoder)}    




# docker tag serasa:latest 385901034746.dkr.ecr.sa-east-1.amazonaws.com/atf/serasa:latest
        
# docker push 385901034746.dkr.ecr.sa-east-1.amazonaws.com/atf/serasa:latest

# aws ecr get-login-password | docker login --username AWS --password-stdin 385901034746.dkr.ecr.sa-east-1.amazonaws.com/modelo3:latest

# curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"text": "SEGMENTO  FACTORINGS\n\nCONFIDENCIAL P/ ALPHATRADE                        DATA 15/12/2015 HORA 10:52:49\nSITUACAO DO CNPJ EM 02/12/2015: ATIVA\nSERASA SOLUCOES EM INFORMACAO                          CNPJ: 02.046.874/0001-05\nRELATO - RELATORIO DE COMPORTAMENTO EM NEGOCIOS        VALORES EM REAIS\n\n\nIDENTIFICACAO / LOCALIZACAO  (ATUALIZACAO EM 04/12/2015)\nCNPJ: 02.046.874/0001-05                                 NIRE: 35.219.893.232\nALPHATRADE SOCIEDADE DE FOMENTO MERCANTIL LTDA\nNOME FANTASIA    : ALPHATRADE SFM\nTIPO DE SOCIEDADE:  SOCIEDADE EMPRESARIA LIMITADA\nOPCAO TRIBUTARIA : LUCRO REAL\nANTECESSORA: ALPHATRADE CIA DE FOMENTO MERCANTIL LTDA           ATE: 17/08/2000\nALPHATRADE ASSESSORIA COML E FINANCEIRA LTDA\nREGISTRO: 35.219.893.232 EM: 14/07/2005\nR DR GERALDO CAMPOS MOREIRA 164 CJ 42\nCIDADE MONCOES - SAO PAULO - SP CEP: 04571-020\nDDD: 11   TEL: 5505-5749\nFUNDACAO: 28/07/1997 FILIAIS: 2 CIDADES: MARINGA, PORTO ALEGRE.\nRAMO: FACTORING E GESTAO DE DIREITOS CREDITORIOS             EMPREGADOS:      4\nCOD. ATIVIDADE SERASA: S-27.00.00\nCNAE: 64.913/00\n\nCONTROLE SOCIETARIO (ATUALIZACAO EM 16/03/2013) (VALORES EM R$)\nCAPITAL SOCIAL:        850.000 REALIZ:          850.000\nORIGEM: BRASIL         CONTROLE: PRIVADO        NATUREZA:   FECHADO\nCPF / CNPJ         ACIONISTA / SOCIO\nENTRADA         NACIONALIDADE            % CAP.VOTANTE   % CAP.TOTAL\n088669459/00       AVELINO DE FREITAS NETO\n07/1997         BRASIL                                        99,9\n292132820/87       ELIZABETH BELTRAN GARCIA\n07/1997         BRASIL                                          ,1\n\nADMINISTRACAO (ATUALIZACAO EM 07/02/2007)\nCPF / CNPJ         ADMINISTRACAO\nCARGO                    NACIONALIDADE   ESTADO CIVIL  ENTRADA      MANDATO\n088669459/00       AVELINO DE FREITAS NETO\nGERENTE                   BRASIL           SOLTEIRO   07/1997       INDET.\n\nREGISTRO DE CONSULTAS\nMES/ANO QTDE    MES/ANO QTDE      CINCO ULTIMAS                            QTDE\nATUAL:    1     MAI 15    1\nNOV/15    0     ABR/15    0       02/12/2015 TIM CELULAR S/A                  1\nOUT/15    1     MAR/15    0       15/10/2015 CALESTINI DISTRIBUIDORA LTDA     1\nSET/15    1     FEV/15    1       08/09/2015 CEF                              1\nAGO/15    0     JAN/15    0       06/05/2015 DAIKIN MCQUAY AR CONDICIONADO B  1\nJUL/15    0     DEZ/14    0       06/02/2015 PILATI MOVEIS LTDA               1\nJUN/15    0     NOV/14    1\n\nANOTACOES DA EMPRESA CONSULTADA\n\nPENDENCIAS FINANCEIRAS\n=== NADA CONSTA PARA O CNPJ CONSULTADO ===\n\nINFORMACOES DO CONCENTRE (VALORES EM REAIS)\nEXISTE APENAS UMA GRAFIA PARA O DOCUMENTO CONSULTADO. ( 02.046.874)\nALPHATRADE SOCIEDADE DE FOMENTO MERCANTIL LTD\nRESUMO\nQTDE  DISCRIMINACAO              PERIODO     OCORRENCIA MAIS RECENTE\nVALOR          ORIGEM     AG/PRACA\n1 PROTESTO                   AGO15-AGO15 R$       1.302 SAO PAULO      SPO\n\nOCORRENCIAS MAIS RECENTES (ATE 05)\n\nPROTESTO\nDATA                      VALOR CARTORIO CIDADE                            UF\n13/08/2015    R$          1.302    05    SAO PAULO                         SP\nTOTAL DE OCORRENCIAS =     1\nVALOR TOTAL =          1.302\n\n=== NADA CONSTA PARA O(S) PARTICIPANTE(S) ===\n\nINFORMACOES DO RECHEQUE (CHEQUES EXTRAVIADOS/SUSTADOS)\n=== NADA CONSTA PARA O CNPJ CONSULTADO ===\n\nCOMPORTAMENTO DE PAGAMENTO DE EMPRESAS\nCOMPORTAMENTO DE PAGAMENTOS\nVALORES EM ATRASO(EM DIAS)      %DOS PAGAMENTOS        VALOR MEDIO\nA VISTA                      95,96%     R$               7.314,11\n8 - 15                        3,21%     R$                 264,96\n16 - 30                        0,68%     R$                  55,89\n31 - 60                        0,15%     R$                  12,12\nACIMA DE 60                      0,00%     R$                   0,00\nTOTAL                        100,00%\n\nVALOR MEDIO DOS PAGAMENTOS EM ATRASO: R$               8.241,81\n\nPRAZO MEDIO DE ATRASO:    1,00  DIAS\n\nVENCIMENTOS FUTUROS\nVALORES A VENCER(EM DIAS)       %DOS PAGAMENTOS        VALOR MEDIO\nATE 10                        1,70%     R$                 246,06\n11 - 30                       70,03%     R$              10.136,80\n31 - 45                        7,31%     R$               1.057,46\n46 - 60                        3,61%     R$                 523,21\nACIMA DE 60                     17,35%     R$               2.510,90\nTOTAL                        100,00%\n\nVALOR MEDIO DOS VALORES A VENCER: R$               7.634,97\n\n_______________________________________________________________________________\nESTE RELATORIO E ESTRITAMENTE CONFIDENCIAL E DESTINADO  A  APOIAR  DECISOES  DE\nCREDITO E NEGOCIOS. E PROIBIDA A REPRODUCAO, TOTAL OU PARCIAL,  BEM   COMO  SUA\nDIVULGACAO A TERCEIROS, POR QUALQUER  FORMA.  A  DECISAO  DE  CONCEDER  OU  NAO\nCREDITO E DE INTEIRA RESPONSABILIDADE  DA  EMPRESA  CONCEDENTE.\n", "file_path": "Teste/test.txt", "txt_type": "LIMPO", "result": 0}'
