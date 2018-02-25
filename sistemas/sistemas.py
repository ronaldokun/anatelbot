from time import sleep

from page import *
from page.page import Page
from sistemas import _locators
from sistemas import _functions


class Sis(Page):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login, senha):

        super().__init__(driver)

        _functions.init_browser(self.driver, login, senha)

    def _navigate(self, link, ident, id_type):

        self.driver.get(link)

        for id in _locators.Entidade[id_type]:

            try:

                elem = self.wait_for_element_to_click(id, timeout=5)

                elem.send_keys(ident + Keys.RETURN)

            except NoSuchElementException:

                print("The html id: {} is not present on this webpage".format(ident))

        else:

            raise ValueError("Não foi encontrado um 'id' html válido nessa página para o identificador {},"
                  " verifique as htmls id's no arquivo 'locators'".format(ident))


    def consulta(self, ident, serv, id_type):

        ident, serv, id_type, sis = _functions.check_input(ident, serv, id_type)

        self._navigate(sis.Consulta, ident, id_type)

    def imprime_consulta(self, ident, serv, id_type):

        self.consulta(ident, serv, id_type)

        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatEstação"))

            elem.click()

        except:

            print("Não foi possível clicar no botão 'Estação' na página consulta")

            return

        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatVersãoparaImpressão"),
                                                  timeout=5)

            elem.click()

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return

    def imprime_boleto(self, ident, id_type):
        """ This function receives a webdriver object, navigates it to the
        loc.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        ident, serv, id_type, sis = _functions.check_input(ident, 'boleto', id_type)

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

        elem.send_keys(ident)

        date = self.wait_for_element_to_click(sis.INPUT_DATA)

        date.clear()

        date.send_keys(_functions.last_day_of_month() + Keys.RETURN)

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

            self.wait_for_new_window()

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

    def incluir_estacao(self, ident, serv, tipo):

        ident, serv, tipo, sis = check_input(ident, serv, tipo)

        self._navigate(sis.Estacao['incluir'], ident, tipo)


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

    page.driver.get(_locators.Sec.Ent_Alt)

    cpf = page.wait_for_element_to_click(_locators.Entidade.cpf)

    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)

    if 'Email' in dados:
        atualiza_campo(dados['Email'], locatos.En.email)

    btn = page.wait_for_element_to_click(locatos.En.bt_dados)

    btn.click()

    if 'RG' in dados:
        atualiza_campo(dados['RG'], locatos.En.rg)

    if 'Orgexp' in dados:
        atualiza_campo(dados['Orgexp'], locatos.En.orgexp)

    if 'Data de Nascimento' in dados:
        data = dados['Data de Nascimento']

        data = data.replace('-', '')

        atualiza_campo(data, locatos.En.nasc)

    btn = page.wait_for_element_to_click(locatos.En.bt_fone)

    btn.click()

    if 'ddd' in dados:

        atualiza_campo(dados['ddd'], locatos.En.ddd)

    else:

        ddd = '11'

        atualiza_campo(ddd, locatos.En.ddd)

        # if 'Fone' in dados:

    #   atualiza_campo(dados['Fone'], Entidade.fone)

    # else:

    #   fone = '123456789'

    #  atualiza_campo(fone, Entidade.fone)

    btn = page.wait_for_element_to_click(locatos.En.bt_end)

    btn.click()

    if 'Cep' in dados:

        cep = dados['Cep']

        cep = cep.replace('-', '')

        atualiza_campo(cep, locatos.En.cep)

        cep = page.wait_for_element_to_click(locatos.En.bt_cep)

        cep.click()

        for i in range(30):

            logr = page.wait_for_element(locatos.En.logr)

            if logr.get_attribute('value'):
                break

            sleep(1)

        else:

            if 'Logradouro' not in dados:
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], locatos.En.logr)

        if 'Número' not in dados:

            raise ValueError("É obrigatório informar o número na atualização\
            do endereço")

        else:

            atualiza_campo(dados['Número'], locatos.En.num)

            if 'Complemento' in dados:
                atualiza_campo(dados['Complemento'], locatos.En.comp)

            bairro = page.wait_for_element(locatos.En.bairro)

            if not bairro.get_attribute('value'):

                if 'Bairro' not in dados:
                    raise ValueError("É obrigatório informar o bairro na atualização\
                                     do endereço")

            else:

                atualiza_campo(dados['Bairro'], locatos.En.bairro)

            # confirmar = page.wait_for_element(Entidade.confirmar)

            # confirmar.click()

            page.driver.execute_script(locatos.En.submit)


def imprime_licenca(page, ident, serv, tipo):
    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)


def consultaSigec(page, ident, tipo='cpf'):
    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:
        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:
        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

    page.driver.get(_locators.Sigec.consulta)

    if tipo in ('cpf', 'cnpj'):

        elem = page.wait_for_element_to_click(_locators.Sigec.cpf)

        elem.send_keys(ident + Keys.RETURN)

    elif tipo == 'fistel':

        elem = page.wait_for_element_to_click(_locators.Sigec.fistel)

        elem.send_keys(ident + Keys.RETURN)

    page.wait_for_page_load()

    # TODO: implement other elements
