from time import sleep

from selenium.webdriver.common.keys import Keys

import sistemas.functions as func
from page import Page
from sistemas.locators import *

USER = 'rsilva'
PASS = 'Savorthemom3nts'


class Sis(Page):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login=USER, senha=PASS):
        super().__init__(driver)

        self.driver.get('http://sistemasnet')

        alert = self.alert_is_present(timeout=3)

        if alert:

            try:

                alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

                alert.accept()

            except:

                print("Não houve necessidade de autenticação no Browser")

    def _navigate(self, link, id, id_type):

        self.driver.get(link)

        for ident in Entidade[id_type]:

            try:

                elem = self.wait_for_element_to_click(ident, timeout=3)

                if elem:
                    elem.send_keys(id + Keys.RETURN)

                    return True

            except:

                print("The html id: {} is not present on this webpage".format(ident))

        else:

            print("Não foi encontrado um 'id' html válido nessa página para o identificador {},"
                  " verifique as htmls id's no arquivo 'locators'".format(id))

            return False

    def consulta(self, id, serv, id_type):

        id, serv, id_type, sis = func.check_input(id, serv, id_type)

        self._navigate(sis.Consulta, id, id_type)

    def imprime_consulta(self, id, serv, id_type):

        self.consulta(id, serv, id_type)



        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatEstação"))

            elem.click()

        except:

            print("Não foi possível clicar no botão 'Estação' na página consulta")

            return

        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatVersãoparaImpressão"),
                                                  timeout=5)

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return


    def imprime_boleto(self, id, id_type):
        """ This function receives a webdriver object, navigates it to the
        loc.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        id, serv, id_type, sis = func.check_input(id, 'boleto', id_type)

        self.driver.get(sis.URL)

        if id_type in ('cpf', 'cnpj'):

            elem = self.wait_for_element_to_click(sis.B_CPF)

            elem.click()

            elem = self.wait_for_element_to_click(sis.INPUT_CPF)

        else:

            elem = self.wait_for_element_to_click(sis.B_FISTEL)

            elem.click()

            elem = self.wait_for_element_to_click(sis.INPUT_FISTEL)

        # self._navigate(sis.URL, id, id_type)

        elem.clear()

        elem.send_keys(id)

        date = self.wait_for_element_to_click(sis.INPUT_DATA)

        date.clear()

        date.send_keys(func.last_day_of_month() + Keys.RETURN)

        #
        # try:
        #
        #     marcar = self.wait_for_element_to_click(sis.MRK_TODOS)
        #
        #     marcar.click()
        #
        #     sleep(5)
        #
        # except:
        #
        #     print("Não foi possível marcar todos os boletos")
        #
        #     return False
        #
        # try:
        #
        #     imprimir = self.wait_for_element_to_click(sis.PRINT)
        #
        #     imprimir.click()
        #
        # except:
        #
        #     print("Não foi possível imprimir todos os boletos")
        #
        #     return False

        try:

            page.wait_for_new_window()

        except:

            print("A espera pela nova janela não funcionou!")

        #
        # try:
        #
        #     windows = page.driver.window_handles
        #
        #     main = windows[0]
        #
        #     boleto = windows[1]
        #
        #     page.driver.switch_to_window(boleto)
        #
        #     save_page(page, ident)
        #
        #
        #
        #     page.close()
        #
        #     page.driver.switch_to_window(main)
        #
        # except:
        #
        #     print("Não foi possível salvar a nova janela")
        #
        #
        #
        #     return False
        #
        # return True

    def save_new_window(self, filename):


        try:

            self.wait_for_new_window(timeout=5)

        except TimeoutError:

            print("Não foi possível identificar a nova Janela para salvar")

            return False

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to_window(windows[-1])

        with open(filename + '.html', 'w') as file:
            # html = soup(driver.page_source).prettify()

            # write image
            file.write(self.driver.page_source)

        self.driver.close()

        self.driver.switch_to_window(windows[0])

        return True








def atualiza_cadastro(page, dados):
    if 'CPF' not in dados:
        raise ValueError("É Obrigatório informar o CPF")

    if len(str(dados['CPF'])) != 11:
        raise ValueError("O CPF deve ter 11 caracteres!")

    def atualiza_campo(data, locator):

        data = str(data)

        elem = page.wait_for_element(locator)

        elem.clear()

        elem.send_keys(data)

        # Navigate to page

    page.driver.get(Sec.Ent_Alt)

    cpf = page.wait_for_element_to_click(Entidade.cpf)

    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)

    if 'Email' in dados:
        atualiza_campo(dados['Email'], Entidade.email)

    btn = page.wait_for_element_to_click(Entidade.bt_dados)

    btn.click()

    if 'RG' in dados:
        atualiza_campo(dados['RG'], Entidade.rg)

    if 'Orgexp' in dados:
        atualiza_campo(dados['Orgexp'], Entidade.orgexp)

    if 'Data de Nascimento' in dados:
        data = dados['Data de Nascimento']

        data = data.replace('-', '')

        atualiza_campo(data, Entidade.nasc)

    btn = page.wait_for_element_to_click(Entidade.bt_fone)

    btn.click()

    if 'ddd' in dados:

        atualiza_campo(dados['ddd'], Entidade.ddd)

    else:

        ddd = '11'

        atualiza_campo(ddd, Entidade.ddd)

        # if 'Fone' in dados:

    #   atualiza_campo(dados['Fone'], Entidade.fone)

    # else:

    #   fone = '123456789'

    #  atualiza_campo(fone, Entidade.fone)

    btn = page.wait_for_element_to_click(Entidade.bt_end)

    btn.click()

    if 'Cep' in dados:

        cep = dados['Cep']

        cep = cep.replace('-', '')

        atualiza_campo(cep, Entidade.cep)

        cep = page.wait_for_element_to_click(Entidade.bt_cep)

        cep.click()

        for i in range(30):

            logr = page.wait_for_element(Entidade.logr)

            if logr.get_attribute('value'):
                break

            sleep(1)

        else:

            if 'Logradouro' not in dados:
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], Entidade.logr)

        if 'Número' not in dados:

            raise ValueError("É obrigatório informar o número na atualização\
            do endereço")

        else:

            atualiza_campo(dados['Número'], Entidade.num)

            if 'Complemento' in dados:
                atualiza_campo(dados['Complemento'], Entidade.comp)

            bairro = page.wait_for_element(Entidade.bairro)

            if not bairro.get_attribute('value'):

                if 'Bairro' not in dados:
                    raise ValueError("É obrigatório informar o bairro na atualização\
                                     do endereço")

            else:

                atualiza_campo(dados['Bairro'], Entidade.bairro)

            # confirmar = page.wait_for_element(Entidade.confirmar)

            # confirmar.click()

            page.driver.execute_script(Entidade.submit)


def incluir_estacao(page, ident, serv, tipo):
    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Estacao['incluir'])

    navigate(page, ident, tipo)


def imprime_licenca(page, ident, serv, tipo):
    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)


def consultaSigec(page, ident, tipo='cpf'):

    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:
        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:
        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

    page.driver.get(Sigec.consulta)

    if tipo in ('cpf', 'cnpj'):

        elem = page.wait_for_element_to_click(Sigec.cpf)

        elem.send_keys(ident + Keys.RETURN)

    elif tipo == 'fistel':

        elem = page.wait_for_element_to_click(Sigec.fistel)

        elem.send_keys(ident + Keys.RETURN)

    page.wait_for_page_load()

    # TODO: implement other elements
