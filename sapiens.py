
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from helpers import Sapiens, Rf_Sapiens
from page import Page

KEYS = ['CPF', 'Nome', 'Mãe', 'Data de Nascimento', 'Sexo',
        'Ano do Óbito','Nacionalidade','Título de Eleitor',
        'Situação Cadastral','Fone', 'Logradouro', 'Número',
        'Complemento', 'Bairro', 'Cidade','Cep']


def tags_to_string(lista_tags):
    reg = []

    for tag in lista_tags:
        for string in tag.stripped_strings:
            reg.append(string)

    # Corrige o registro de nome e endereço
    reg[0] = reg[0] + reg[1]

    reg.remove(reg[1])

    reg[1] = reg[1] + reg[2]

    reg.remove(reg[2])

    return reg


def cria_dict_dados(registros):

    dados = {}

    chaves = ['CPF', 'Nome', 'Mãe', 'Data de Nascimento', 'Sexo',
              'Ano do Óbito', 'Nacionalidade', 'Título de Eleitor',
              'Situação Cadastral', 'Fone']

    for s in registros:

        s = s.split(':')

        if s[0] in chaves:
            dados[s[0]] = s[1].lstrip(' ')

    if len(registros) >= 2:
        endereco = registros[-2].split(',')

    if len(endereco) == 6:

        items_end = ['Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade',
                     'Cep']
    elif len(endereco) == 5:

        items_end = ['Logradouro', 'Número', 'Bairro', 'Cidade', 'Cep']

    if items_end:

        for k, v in zip(items_end, endereco):
            dados[k] = v.lstrip(' ')

    # corrige CEP
    if 'Cep' in dados:
        dados['Cep'] = dados['Cep'][-9:]

    return dados


class LoginPage(Page):

    def login(self, usr, pwd):
        """
        make login and return and instance of browser"""

        self.driver.get(Sapiens.URL)
        self.driver.maximize_window()

        usuario = self.wait_for_element_to_click(Sapiens.LOGIN)
        senha = self.wait_for_element_to_click(Sapiens.SENHA)

        # Clear any clutter on the form
        usuario.clear()
        usuario.send_keys(usr)

        senha.clear()
        senha.send_keys(pwd)

        # Hit Enter
        senha.send_keys(Keys.RETURN)

        return Page_sapiens(self.driver)


class Page_sapiens(Page):

    def __init__(self, driver):
        self.driver = driver
        self.registros = {}

    def add_registro(self, registro):

        key, value = registro

        if key not in self.registros or self.get_registro[key] is None:
            self.registros[key] = value

    def get_registro(self, cpf):
        """

        :type cpf: string
        """
        return self.registros.get(cpf, None)

    def go_to_RF(self):
        self.driver.get(Rf_Sapiens.URL)

    def pesquisa_obito(self, cpf):

        if self.get_url != Rf_Sapiens.URL:
            with self.wait_for_page_load():
                self.go_to_RF()

        entidade = self.wait_for_element((By.ID, "textfield-1014-inputEl"))
        entidade.clear()

        entidade.send_keys(str(cpf) + Keys.RETURN)

        try:

            elem = self.elem_is_visible((By.CLASS_NAME, "x-grid-cell-inner"))

            if "Óbito" in str(elem.text):
                return "OBITO"
            else:
                return "ATIVO"

        except:
            print("Problema ao resgatar o elemento da busca")
            return ""

    def pesquisa_dados(self, cpf):

        if self.get_url != Rf_Sapiens.URL:
            with self.wait_for_page_load():
                self.go_to_RF()

        entidade = self.wait_for_element(Rf_Sapiens.IDINPUTCPF)
        entidade.clear()

        entidade.send_keys(str(cpf) + Keys.RETURN)

        if self.check_element_exists(Rf_Sapiens.RESULTADO):

            html = soup(self.driver.page_source, "lxml")

            resultado = html.find('tr', {'data-recordid': str(cpf)})

            try:
                resultado = [content.div for content in resultado.contents]
            except:
                print('Resultado não possui atributos contents para o CPF: {}'.format(cpf))
                resultado = None
        else:

            resultado = None

        if resultado is not None:

            resultado = tags_to_string(resultado)

            resultado = cria_dict_dados(resultado)

            self.add_registro((cpf, resultado))


