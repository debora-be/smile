import requests, logging
import time
import csv
from bs4 import BeautifulSoup



logging.basicConfig(filename='log_ficha_completa.log')

                
# obter numeros das fichas cadastrais #
def pega_codigos_pacientes():
    lista_codigo_paciente = []

    for i in range(1, 221):
        print('Pegando informações da pagina {}'.format(i))
        home_page = requests.get('http://masteripat.ddns.net:81/gco/pacientes/pesquisa_ajax.php?pesquisa=&campo=nome&pg={}'.format(i), cookies={
            'PHPSESSID': 'qasa4a1etcncq5kpqdgg5195i0'
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
        time.sleep(0.5)

    return lista_codigo_paciente 



# acessa dados completos da ficha cadastral de cada paciente #
def pega_ficha_cadastral(codigos_dos_pacientes):
    ficha_cadastral_list = []
    print('CODIGOS DOS PACIENCITES:', codigos_dos_pacientes)
    for i in codigos_dos_pacientes:
        print("Ficha cadastral número {}".format(i))
        ficha_cadastral = {}

        ficha = requests.get('http://masteripat.ddns.net:81/gco/relatorios/paciente.php?codigo={}'.format(i), cookies={
            'PHPSESSID': 'qasa4a1etcncq5kpqdgg5195i0'
            })


        # localiza tabela de informações pessoais #
        ficha_content = BeautifulSoup(ficha.text, 'html.parser')
        tables_all = ficha_content.find_all('table')
        table_info_pessoal = tables_all[3]
        table_info_extra = tables_all[7]


        # pega e trata informações pessoais #
        logging.info('Acessando ficha cadastral do paciente {}'.format(i))
        for item in table_info_pessoal:
            try:       
                if item.text != "":
                    all_tds = item.find_all('td')
                    for td in all_tds:
                        td_text = td.text.replace(u'\xa0', '').strip().split(':')
                        chave = td_text[0]
                        valor = td_text[1].replace('\n', '').replace('\r', '')                        
                        ficha_cadastral.update({chave: valor})
     
            except Exception as e:
                pass
        time.sleep(0.5)   


        # pega e trata informações extras #
        for item in table_info_extra:
            try:       
                if item.text != "":
                    all_tds = item.find_all('td')
                    for td in all_tds:
                        td_text = td.find('td').text.replace(u'\xa0', '').strip().split(':')
                        chave = td_text[0]
                        valor = td_text[1].replace('\n', '').replace('\r', '')
                        #print('CHAVE:', chave, 'VALOR: ', valor)
                        if 'FACEBOOK' in valor:
                            valor = ''
                        ficha_cadastral.update({chave: valor})
                   
                
            except Exception as e:
                pass

        time.sleep(0.5)
        
        ficha_cadastral_list.append(ficha_cadastral)
        
    
    return ficha_cadastral_list



# cria arquivo csv e exporta #
def register_info_in_csv(ficha_cadastral_list):
    with open('pacientes_ficha_completa.csv', 'w') as csvfile:
        linha = 1
        csvwriter = csv.writer(csvfile)
           
        for ficha in ficha_cadastral_list:
            if linha == 1:
                csvwriter.writerow(ficha.keys())
                csvwriter.writerow(ficha.values())
                linha += 1
            else:
                csvwriter.writerow(ficha.values())

        

###########INÍCIO DO PROGRAMA###########

codigo_dos_pacientes = pega_codigos_pacientes()

ficha_cadastral = pega_ficha_cadastral(codigo_dos_pacientes)
print(ficha_cadastral)

print('\n\n\n INICIANDO ESCRITA DO ARQUIVO EXCEL!')
register_info_in_csv(ficha_cadastral)