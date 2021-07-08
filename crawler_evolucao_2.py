import requests, logging
import time
import csv
from bs4 import BeautifulSoup

logging.basicConfig(filename='log_evolucao_tratamento.log')



# obter numeros das fichas cadastrais #
def pega_codigos_pacientes():
    lista_codigo_paciente = []

    for i in range(1, 2):
        print('Pegando informações da pagina {}'.format(i))
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



# acessar evolução do tratamento de cada paciente #
def pega_evolucao_tratamento(codigos_dos_pacientes):

    print('CODIGOS DOS PACIENTES:', codigos_dos_pacientes)
    
    for i in codigos_dos_pacientes:
        r = requests.get('http://masteripat.ddns.net:81/gco/relatorios/evolucao.php?codigo={}'.format(i), cookies={
            'PHPSESSID': 'gi76r5ggb8k9c3q553rfs67151'
            })

        # localiza todas as fonts #
        evolucao_content = BeautifulSoup(r.text, 'html.parser')
        all_fonts = evolucao_content.find_all('font')
        
        # pega e trata o nome do paciente na font #
        nome_paciente_font = all_fonts[3]
        nome_paciente = nome_paciente_font.find('b').text
        print('Evolução do tratamento do paciente', nome_paciente)

        # pega conteúdo do tratamento #  
        all_tables = evolucao_content.find_all('table')
        procedimentos_paciente_table = all_tables[2].text

        # cria dicionario paciente #
        logging.info('Acessando tratamento do paciente {}'.format(i))
        #for item in procedimentos_paciente_table:
        paciente_evolucao_dict = {'nome paciente': nome_paciente} #{'procedimentos': [
                    #item[0, 1, 2, 3]
               # ]
           # }

            
        print(paciente_evolucao_dict)   

    
 

###########INÍCIO DO PROGRAMA###########

codigo_dos_pacientes = pega_codigos_pacientes()

pega_evolucao_tratamento(codigo_dos_pacientes)

