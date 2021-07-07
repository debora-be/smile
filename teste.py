import requests, logging
import time
import csv
from bs4 import BeautifulSoup

logging.basicConfig(filename='log_evolucao.log')



# obter numeros das fichas cadastrais
def pega_codigos_pacientes():
    lista_codigo_paciente = []

    for i in range(1, 2):
        print("Pegando informações da pagina {}".format(i))
        home_page = requests.get('http://masteripat.ddns.net:81/gco/pacientes/pesquisa_ajax.php?pesquisa=&campo=nome&pg={}'.format(i), cookies={
            'PHPSESSID': 'm6qp058b8dnqufqtnvf8bokih6'
        })

        home_page_content = BeautifulSoup(home_page.text, 'html.parser')
        td_lista = home_page_content.find_all('td')

        for item in td_lista:
            try:
                if item.text != "":
                    lista_codigo_paciente.append(int(item.text))
            except:
                print('Não é possivel passar o item.text pra numero inteiro.')
                pass

    return lista_codigo_paciente 



# acessar evolução do tratamento de cada paciente
def pega_evolucao_tratamento(codigos_dos_pacientes):
    evolucao_tratamento_list = []
    print('CODIGOS DOS PACIENTES:', codigos_dos_pacientes)
    
    for i in codigos_dos_pacientes:
        print('Evolução do tratamento do paciente')
        evolucao = requests.get('http://masteripat.ddns.net:81/gco/pacientes/evolucao_ajax.php?codigo={}&acao=editar'.format(i), cookies={
            'PHPSESSID': 'gi76r5ggb8k9c3q553rfs67151'
            })


# localiza evolução do tratamento de cada paciente
        evolucao_content = BeautifulSoup(evolucao.text, 'html.parser')
        evolucao = evolucao_content.find_all('td')


# pega somente o nome do paciente na td
        for item in evolucao:
            evolucao_dict = {}
            try:
                if item.text != "":
                    nome = item.find_all('b')
                    nome_text = item.text.replace(
                        'Gerenciar Pacientes', '')
                    nome_text_2 = nome_text.replace(
                        ']', '')
                    nome_paciente = nome_text_2.replace(
                        '[', '')
                    print(nome_paciente)
            
            except Exception as e:
                print('Não está sendo possível pegar os dados', e)
                pass


 # pega identificação e tratamentos do paciente nas tables [3] e [4]
        tables_all = evolucao_content.find_all('table')
        table_identificacao = tables_all[3]
        table_evolucao = tables_all[4]

        for item in table_evolucao:
            evolucao_dict = {}
            try:
                if item.text != "":
                    #procedimento_executado = 
                    #procedimento_previsto = 
                    #profissional = 
                    #data = 
                    #nome = item.find_all('b')
                    #nome_text = item.text.replace(
                     #   'Gerenciar Pacientes', '')
                    #nome_text_2 = nome_text.replace(
                    #    ']', '')
                    #nome_paciente = nome_text_2.replace(
                    #    '[', '')
                    print(table_evolucao)
            
            except Exception as e:
                print('Não está sendo possível pegar os dados', e)
                pass           
            #evolucao_dict.update({'Evolução do tratamento do paciente', nome_paciente})

             #  orcamento_unico_content = BeautifulSoup(orcamento_unico.text, 'html.parser')
              #  tag_fonts = orcamento_unico_content.find_all('font')
              #  tag_fonts_orc_para = tag_fonts[3].text.split(':')
              #  tag_fonts_orc_com = tag_fonts[5].text.split('com ')
   
               # orcamento_dict.update({'Orçamento para': tag_fonts_orc_para[1].strip()})
              #  orcamento_dict.update({'Tratamento com': tag_fonts_orc_com[1].strip()})
              #  print(orcamento_dict)

# pega table com o tratamento do paciente 


        
            

    
#orcamento_content = BeautifulSoup(orcamentos.text, 'html.parser')
      #  all_tables = orcamento_content.find_all('table')
      #  table = all_tables[6]

       # for item in table.find_all('tr'):
          #  orcamento_dict = {}
          #  try:
              #  td_btn_edit = item.find_all('td')[4].find('a')['href']
              #  url_params_list = td_btn_edit.split('&')
               # cod_orcamento = url_params_list[-1].replace('codigo_orc=', '').replace("')", '')

                ### ACESSANDO ORCAMENTO UNICO ###
               # logging.info('Acessando orcamento {} do usuario {}'.format(cod_orcamento, i))
               # orcamento_unico = requests.get('http://masteripat.ddns.net:81/gco/relatorios/orcamento.php?codigo={}'.format(cod_orcamento), cookies={
              #  'PHPSESSID': 'm6qp058b8dnqufqtnvf8bokih6'
             #   })

              #  orcamento_unico_content = BeautifulSoup(orcamento_unico.text, 'html.parser')
              #  tag_fonts = orcamento_unico_content.find_all('font')
              #  tag_fonts_orc_para = tag_fonts[3].text.split(':')
              #  tag_fonts_orc_com = tag_fonts[5].text.split('com ')
   
               # orcamento_dict.update({'Orçamento para': tag_fonts_orc_para[1].strip()})
              #  orcamento_dict.update({'Tratamento com': tag_fonts_orc_com[1].strip()})
              #  print(orcamento_dict)


    # LOCALIZA TABELA DE INFORMAÇÕES PESSOAS #
        #ficha_content = BeautifulSoup(ficha.text, 'html.parser')
       # tables_all = ficha_content.find_all('table')
        #table_info_pessoal = tables_all[3]
        #table_info_extra = tables_all[7]

       # # PEGA E TRATA INFORMAÇÕES PESSOAIS #
        #for item in table_info_pessoal:
            #try:
                   # if item.text != "":
                        #all_tds = item.find_all('td')
                        #for td in all_tds:
                           # td_text = td.text.replace(
                            #    u'\xa0', '').strip().split(':')
                           # chave = td_text[0]
                           # valor = td_text[1].replace('\n', '').replace('\r', '')
                          # ficha_cadastral.update({chave: valor})

                #except Exception as e:
                 #   pass

    #PEGA E TRATA INFORMAÇÕES EXTRAS #
        #for item in table_info_extra:
           # try:       
               # if item.text != "":
                  #  all_tds = item.find_all('td')
                  #  for td in all_tds:
                      #  td_text = td.find('td').text.replace(u'\xa0', '').strip().split(':')
                      #  chave = td_text[0]
                      #  valor = td_text[1].replace('\n', '').replace('\r', '')
                        #print('CHAVE:', chave, 'VALOR: ', valor)
                      #  if 'FACEBOOK' in valor:
                          #  valor = ''
                      #  ficha_cadastral.update({chave: valor})

                     # except Exception as e:
                #pass
        
        #time.sleep(1)
      #  ficha_cadastral_lista.append(ficha_cadastral)
        
    
  #  return ficha_cadastral_lista

###########INÍCIO DO PROGRAMA#######

codigo_dos_pacientes = pega_codigos_pacientes()

pega_evolucao_tratamento(codigo_dos_pacientes)


