import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


# obter numeros das fichas cadastrais
def pega_codigos_pacientes():
    lista_codigo_paciente = []

    for i in range(1, 2):
        print("Pegando informações da pagina {}".format(i))
        home_page = requests.get('http://masteripat.ddns.net:81/gco/pacientes/pesquisa_ajax.php?pesquisa=&campo=nome&pg={}'.format(i), cookies={
            'PHPSESSID': 'sauem0dljbi0cptho8p1kig6m5'
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



# acessar orçamento(s) de cada paciente
def pega_orcamento_paciente(codigos_dos_pacientes):
    orcamento_paciente = []
    for i in codigos_dos_pacientes:
        print("Orçamento(s) paciente número {}".format(i))
        orcamento = requests.get('http://masteripat.ddns.net:81/gco/pacientes/orcamento_ajax.php?codigo={}&acao=editar'.format(i), cookies={
            'PHPSESSID': 'sauem0dljbi0cptho8p1kig6m5'
            })

        orcamento_content = BeautifulSoup(orcamento.text, 'html.parser')
        orcamento = orcamento_content.find_all('td')
    
        for item in orcamento:
            try:
                if item.text != "":
                    print(item.text)
            except Exception as e:
                print('Não está sendo possível pegar os dados', e)
        print(pd.DataFrame(item.text))


### INICIO DO PROGRAMA ###
codigo_dos_pacientes = pega_codigos_pacientes()

pega_orcamento_paciente(codigo_dos_pacientes)