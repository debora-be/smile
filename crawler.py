import requests
import time
from bs4 import BeautifulSoup


# obter numeros das fichas cadastrais
def pega_codigos_pacientes():
    lista_codigo_paciente = []

    for i in range(1, 20):
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



# acessar dados completos da ficha cadastral de cada paciente
def pega_ficha_cadastral(codigos_dos_pacientes):
    ficha_cadastral = []
    for i in codigos_dos_pacientes:
        print("Ficha cadastral número {}".format(i))
        ficha = requests.get('http://masteripat.ddns.net:81/gco/relatorios/paciente.php?codigo={}'.format(i), cookies={
            'PHPSESSID': 'sauem0dljbi0cptho8p1kig6m5'
            })

        ficha_content = BeautifulSoup(ficha.text, 'html.parser')
        ficha = ficha_content.find_all('td')
    
        for item in ficha:
            try:
                if item.text != "":
                    print(item.text)
            except Exception as e:
                print('Não está sendo possível pegar os dados', e)
   
   
                
# acessar evolução do tratamento de cada paciente
def pega_evolucao_tratamento(codigos_dos_pacientes):
    evolucao_tratamento = []
    for i in codigos_dos_pacientes:
        print("Evolução do tratamento do paciente número {}".format(i))
        evolucao = requests.get('http://masteripat.ddns.net:81/gco/pacientes/evolucao_ajax.php?codigo={}&acao=editar'.format(i), cookies={
            'PHPSESSID': 'sauem0dljbi0cptho8p1kig6m5'
            })

        evolucao_content = BeautifulSoup(evolucao.text, 'html.parser')
        evolucao = evolucao_content.find_all('td')
    
        for item in evolucao:
            try:
                if item.text != "":
                    print(item.text)
            except Exception as e:
                print('Não está sendo possível pegar os dados', e)



# acessar orçamento(s) de cada paciente
def pega_orcamento_paciente(codigos_dos_pacientes):
    orcamento_paciente = []
    for i in codigos_dos_pacientes:
        print("Orçamento(s) do paciente número {}".format(i))
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



### INICIO DO PROGRAMA ###
codigo_dos_pacientes = pega_codigos_pacientes()

pega_ficha_cadastral(codigo_dos_pacientes)

pega_evolucao_tratamento(codigo_dos_pacientes)

pega_orcamento_paciente(codigo_dos_pacientes)