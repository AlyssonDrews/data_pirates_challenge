from urllib.parse import urlencode
from urllib.request import Request, urlopen

import glob, os, codecs, sys
import json
import constants
from bs4 import BeautifulSoup


##Create Document##
def create_and_write_document(dir_name, name_uf, data):
    with open('./{}/{}.jsonl'.format(dir_name, name_uf), 'w+', encoding='utf-8') as output:
        output.write('{ CEP: [')
        for line in data:
            output.write(json.dumps(line, ensure_ascii=False) + ',\n')
        output.write(']}')

##Get data from URL##
def get_data(req):
    soup = BeautifulSoup(req, 'html.parser')
    return soup.find_all('table')[1]

def build_info(data, qtdrow = 100):
        return [ {
            'Localidade' : td.find_all('td')[0].get_text(),
            'Faixa de CEP': td.find_all('td')[1].get_text()
        }
        for td in data.findAll('tr')[2:2 + qtdrow]
        ]
def clean_data(data):
    address_list = build_info(data)
    remove_duplicates = {each ['Localidade'] : each for each in address_list}.values()
    return remove_duplicates

if __name__ == '__main__':
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCep.cfm'
    for uf in constants.UF_LIST:
        fields = {"UF": uf, 'Localidade': '', 'qtdrow' : '100', 'pagini': '1', 'pagfim' : '101' }
        request = Request(url, urlencode(fields).encode())
        result = urlopen(request).read()
        data = get_data(result)
        address = clean_data(data)
        print(data)
        dir_name = constants.NAME_OF_DIRECTORY
        try:
            os.mkdir(dir_name)
            create_and_write_document(dir_name, uf, address)
        except FileExistsError:
            create_and_write_document(dir_name, uf, address)