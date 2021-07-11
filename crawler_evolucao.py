import requests, logging
import time
import csv
from bs4 import BeautifulSoup


logging.basicConfig(filename='log_evolucao_tratamento.log')


                
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

    return lista_codigo_paciente 



# acessar evolução do tratamento de cada paciente #
def pega_evolucao_tratamento(codigos_dos_pacientes):
    tratamentos_list = []

    print('CODIGOS DOS PACIENTES:', codigos_dos_pacientes)
    
    for i in codigos_dos_pacientes:
        r = requests.get('http://masteripat.ddns.net:81/gco/relatorios/evolucao.php?codigo={}'.format(i), cookies={
            'PHPSESSID': 'qasa4a1etcncq5kpqdgg5195i0'
            })

        # localiza todas as fonts #
        evolucao_content = BeautifulSoup(r.text, 'html.parser')
        all_fonts = evolucao_content.find_all('font')
        
        # pega e trata o nome do paciente na font #
        nome_paciente_font = all_fonts[3]
        nome_paciente = nome_paciente_font.find('b').text
        print('Evolução do tratamento do paciente', nome_paciente)

        # pega conteúdo do tratamento do paciente #  
        all_tables = evolucao_content.find_all('table')
        table_rows = all_tables[2].find_all('tr')
    
    
        #table_row = table_rows.text


        #procedimentos_paciente = table_row.text.replace('\n', '')

        # cria dicionario paciente #
        logging.info('Criando ficha com informações do tratamento do paciente {}'.format(i))
        paciente_evolucao_dict = {
            'nome_paciente': nome_paciente,
            'procedimentos': []
        }

        del table_rows[0]

        for linha in table_rows:
            all_tds = linha.find_all('td')

            procedimento_dict = {
                'procedimento_executado': '',
                'procedimento_previsto': '',
                'profissional': '',
                'data': ''
            }            
            
            for coluna in all_tds:
                procedimento_dict.update({'procedimento_executado': all_tds[0].text.strip()})
                procedimento_dict.update({'procedimento_previsto': all_tds[1].text.strip()})
                procedimento_dict.update({'profissional': all_tds[2].text.strip()})
                procedimento_dict.update({'data': all_tds[3].text.strip()})

            paciente_evolucao_dict['procedimentos'].append(procedimento_dict)

        tratamentos_list.append(paciente_evolucao_dict)

    return tratamentos_list



# cria arquivo csv e exporta #
def register_info_in_csv(tratamento_list):
    with open('pacientes_evolucao_tratamento.csv', 'w') as csvfile:
        linha = 1
        csvwriter = csv.writer(csvfile)
           
        for tratamento in tratamento_list:
            if linha == 1:
                csvwriter.writerow(tratamento.keys())
                csvwriter.writerow(tratamento.values())
                linha += 1
            else:
                csvwriter.writerow(tratamento.values())



###########INÍCIO DO PROGRAMA###########

codigo_dos_pacientes = pega_codigos_pacientes()

evolucao_tratamento = pega_evolucao_tratamento(codigo_dos_pacientes)
print(evolucao_tratamento)

print('\n\n\n INICIANDO ESCRITA DO ARQUIVO EXCEL!')
register_info_in_csv(evolucao_tratamento)