from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys

from sistemas import sis_helpers as h

from sistemas.sis_helpers import Rf_Sapiens
from page import Page
import pandas as pd

KEYS = [
    "CPF",
    "Nome",
    "Mãe",
    "Data de Nascimento",
    "Sexo",
    "Ano do Óbito",
    "Nacionalidade",
    "Título de Eleitor",
    "Situação Cadastral",
    "Fone",
    "Logradouro",
    "Número",
    "Complemento",
    "Bairro",
    "Cidade",
    "Cep",
]

ACOES = ["incluir_doc", "ini"]


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

    chaves = [
        "CPF",
        "Nome",
        "Mãe",
        "Data de Nascimento",
        "Sexo",
        "Ano do Óbito",
        "Nacionalidade",
        "Título de Eleitor",
        "Situação Cadastral",
        "Fone",
    ]

    for s in registros:

        s = s.split(":")

        if s[0] in chaves:
            dados[s[0]] = s[1].lstrip(" ")

    if len(registros) >= 2:
        endereco = registros[-2].split(",")

        items_end = []

        if len(endereco) == 6:

            items_end = [
                "Logradouro",
                "Número",
                "Complemento",
                "Bairro",
                "Cidade",
                "Cep",
            ]
        elif len(endereco) == 5:

            items_end = ["Logradouro", "Número", "Bairro", "Cidade", "Cep"]

        if items_end:

            for k, v in zip(items_end, endereco):
                dados[k] = v.lstrip(" ")

    # corrige CEP
    if "Cep" in dados:
        dados["Cep"] = dados["Cep"][-9:]

    return dados


class LoginPage(Page):
    def login(self, usr, pwd):
        """
        make login and return and instance of browser"""

        self.driver.get(h.Sapiens.URL)
        self.driver.maximize_window()

        usuario = self.wait_for_element_to_click(h.Sapiens.LOGIN)
        senha = self.wait_for_element_to_click(h.Sapiens.SENHA)

        # Clear any clutter on the form
        usuario.clear()
        usuario.send_keys(usr)

        senha.clear()
        senha.send_keys(pwd)

        # Hit Enter
        senha.send_keys(Keys.RETURN)

        return Sapiens(self.driver)


class Sapiens(Page):
    def __init__(self, driver, registros=None):
        self.driver = driver
        if registros is None:
            self.registros = dict()

        else:
            self.registros = registros

    def reiniciar_driver(self, driver):

        self.fechar()

        self.driver = driver

    def add_registro(self, registro):

        key, value = registro

        self.registros[key] = value

    def get_registro(self, cpf):
        """

        :type cpf: string
        """
        return self.registros.get(cpf, None)

    def saveas_dataframe(self):

        df = pd.Dataframe(columns=KEYS)

        for k, v in self.registros.items():

            registro = pd.Series(v.values())

            registro["CPF"] = k

            df = df.append(registro, ignore_index=True)

        return df

    def go_to_RF(self):

        self.driver.get(Rf_Sapiens.URL)

    def pesquisa_dados(self, cpf):

        if self.get_url != Rf_Sapiens.URL:
            with self.wait_for_page_load():
                self.go_to_RF()

        if len(cpf) == 11:

            # self._click_button((By.LINK_TEXT, "Pessoas Físicas"))

            # self._click_button(Rf_Sapiens.BTN_PF)

            id_input = Rf_Sapiens.ID_INPUT_CPF

        elif len(cpf) == 14:

            # self._click_button((By.LINK_TEXT, "Pessoas Jurídicas"))

            self._clicar(Rf_Sapiens.BTN_PJ, 1)

            id_input = Rf_Sapiens.ID_INPUT_CNPJ

        else:

            raise ValueError("Número identificador inválido {}".format(cpf))

        self._atualizar_elemento(id_input, dado=str(cpf) + Keys.RETURN)

        if self.check_element_exists(Rf_Sapiens.RESULTADO):

            html = soup(self.driver.page_source, "lxml")

            resultado = html.find("tr", {"data-recordid": str(cpf)})

            try:
                resultado = [content.div for content in resultado.contents]
            except:
                print(
                    "Resultado não possui atributos contents para o CPF: {}".format(cpf)
                )
                resultado = None
        else:

            resultado = None

        if resultado:

            resultado = tags_to_string(resultado)

            resultado = cria_dict_dados(resultado)

            self.add_registro((cpf, resultado))

