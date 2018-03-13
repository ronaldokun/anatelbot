from time import sleep

from page import *

import helpers
import functions

SERVICOS = ["cidadao", "radioamador", "maritimo", "aeronautico", "boleto", "sec"]

PATTERNS = [r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$',
            r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$',
            r'^(P){1}([A-Z]){4}$',
            r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})']

TIPOS_ESTACAO = ["Fixa", "Móvel"]


class Scpx(Page):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login, senha):

        self.sistema = helpers.Scpx

        self.tipo = 'cpf'

        super().__init__(driver)

        functions.init_browser(self.driver, login, senha)

    def _navigate(self, identificador, tipo, link, id, go=True):

        identificador = str(identificador)

        if not functions.check_input(identificador, tipo):
            raise ValueError("Identificador inválido: ", identificador)

        with self.wait_for_page_load():

            self.driver.get(link)

        with self.wait_for_page_load():

            try:

                elem = self.wait_for_element_to_click(id, timeout=10)

                elem.send_keys(identificador + Keys.RETURN)

            except NoSuchElementException:

                print("The html id: {} is not present on this webpage".format(ident))


    def consulta(self, identificador, tipo='cpf'):

        self._navigate(identificador, tipo, self.sistema.Consulta['link'], self.sistema.Consulta[tipo])


    def imprime_consulta(self, identificador, tipo='cpf', resumida=False):

        self.consulta(identificador, tipo)

        try:

            elem = self.wait_for_element_to_click(self.sistema.Consulta['btn_estacao'])

            elem.click()

        except:

            print("Não foi possível clicar no botão 'Estação' na página consulta")

            return

        try:

            if resumida:

                self.driver.execute_script("VersaoImpressao('R')")

            else:

                self.driver.execute_script("VersaoImpressao('N')")


        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return


    def incluir_serviço(self, identificador, tipo='cpf'):

        self._navigate(identificador, tipo, self.sistema.Servico['incluir'], self.sistema.Consulta[tipo])

    def incluir_estacao(self, identificador, tipo_estacao, indicativo, sequencial,  tipo='cpf', uf='SP'):

        if tipo_estacao not in TIPOS_ESTACAO:
            raise ValueError("Os tipos de estação devem ser: ".format(TIPOS_ESTACAO))

        self._navigate(identificador, tipo, self.sistema.Estacao['incluir'], self.sistema.Consulta[tipo])

        button = self.wait_for_element_to_click(self.sistema.Estacao['btn_dados_estacao'])

        button.click()

        estado = Select(self.wait_for_element(self.sistema.Estacao['uf']))

        estado.select_by_value(uf)

        indic= self.wait_for_element(self.sistema.Estacao['indicativo'])

        indic.send_keys(indicativo)

        seq = self.wait_for_element(self.sistema.Estacao["seq"])

        seq.send_keys(sequencial)

        tipo_est = Select(self.wait_for_element(self.sistema.Estacao['tipo']))

        if tipo_estacao == 'Móvel':

            tipo_est.select_by_visible_text("Móvel")

        elif tipo_estacao == "Fixa":

            tipo_est.select_by_visible_text("Fixa")

        else:

            tipo_est.select_by_visible_text("Telecomando")

        confirmar = self.wait_for_element_to_click(self.sistema.Estacao['confirmar'])

        with self.wait_for_page_load(): confirmar.click()

    def aprovar_movimento(self, identificador, origem, tipo='cpf'):

        try:
            self._navigate(identificador, tipo, self.sistema.Movimento['transferir'], self.sistema.Consulta[tipo], False)

        except UnexpectedAlertPresentException:

            pass


        movimento_atual = Select(self.wait_for_element_to_click(self.sistema.Movimento['atual']))

        if origem.lower() == "a":

            movimento_atual.select_by_visible_text("A - Em Análise")

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['confirmar'])

            with self.wait_for_page_load(): confirmar.click()

            movimento_a_transferir = Select(self.wait_for_element_to_click(self.sistema.Movimento['posterior']))

            movimento_a_transferir.select_by_visible_text("")


        elif origem.lower() == "b":

            movimento_atual.select_by_visible_text(("B - Cadastro pela Anatel"))

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['confirmar'])

            with self.wait_for_page_load(): confirmar.click()

            movimento_a_transferir = Select(self.wait_for_element_to_click(self.sistema.Movimento['posterior']))

            movimento_a_transferir.select_by_visible_text("E - Aprovado / Licença")

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['confirmar'])

            with self.wait_for_page_load(): confirmar.click()

    def licenciar_estacao(self, identificador, tipo='cpf', ppdess=True):

        if not ppdess:

            self._navigate(identificador, tipo, self.sistema.Estacao['licenciar'], self.sistema.Consulta[tipo], False)

            if tipo == 'cpf':

                cpf = self.wait_for_element_to_click((By.LINK_TEXT, identificador))

                cpf.click()


            lista_estacoes = self.wait_for_element_to_click(self.sistema.Estacao['btn_lista_estacoes'])

            lista_estacoes.click()

            self.wait_for_element_to_click(self.sistema.Estacao['btn_licenciar']).click()

            return

        else:

            self._navigate(identificador, tipo, self.sistema.Estacao['licenciar'], self.sistema.Consulta[tipo], False)

            if tipo == 'cpf':

                cpf = self.wait_for_element_to_click((By.LINK_TEXT, identificador))

                cpf.click()

                return

            #alert.accept()





    def imprime_boleto(self, ident, id_type):
        """ This function receives a webdriver object, navigates it to the
        loc.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        ident, serv, id_type, sis = functions.check_input(ident, id_type)

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

        date.send_keys(functions.last_day_of_month() + Keys.RETURN)

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

    page.driver.get(helpers.Sec.Ent_Alt)

    cpf = page.wait_for_element_to_click(helpers.Entidade.cpf)

    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)

    if 'Email' in dados:
        atualiza_campo(dados['Email'], helpers.En.email)

    btn = page.wait_for_element_to_click(helpers.En.bt_dados)

    btn.click()

    if 'RG' in dados:
        atualiza_campo(dados['RG'], helpers.En.rg)

    if 'Orgexp' in dados:
        atualiza_campo(dados['Orgexp'], helpers.En.orgexp)

    if 'Data de Nascimento' in dados:
        data = dados['Data de Nascimento']

        data = data.replace('-', '')

        atualiza_campo(data, helpers.En.nasc)

    btn = page.wait_for_element_to_click(helpers.En.bt_fone)

    btn.click()

    if 'ddd' in dados:

        atualiza_campo(dados['ddd'], helpers.En.ddd)

    else:

        ddd = '11'

        atualiza_campo(ddd, helpers.En.ddd)

        # if 'Fone' in dados:

    #   atualiza_campo(dados['Fone'], Entidade.fone)

    # else:

    #   fone = '123456789'

    #  atualiza_campo(fone, Entidade.fone)

    btn = page.wait_for_element_to_click(helpers.En.bt_end)

    btn.click()

    if 'Cep' in dados:

        cep = dados['Cep']

        cep = cep.replace('-', '')

        atualiza_campo(cep, helpers.En.cep)

        cep = page.wait_for_element_to_click(helpers.En.bt_cep)

        cep.click()

        for i in range(30):

            logr = page.wait_for_element(helpers.En.logr)

            if logr.get_attribute('value'):
                break

            sleep(1)

        else:

            if 'Logradouro' not in dados:
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], helpers.En.logr)

        if 'Número' not in dados:

            raise ValueError("É obrigatório informar o número na atualização\
            do endereço")

        else:

            atualiza_campo(dados['Número'], helpers.En.num)

            if 'Complemento' in dados:
                atualiza_campo(dados['Complemento'], helpers.En.comp)

            bairro = page.wait_for_element(helpers.En.bairro)

            if not bairro.get_attribute('value'):

                if 'Bairro' not in dados:
                    raise ValueError("É obrigatório informar o bairro na atualização\
                                     do endereço")

            else:

                atualiza_campo(dados['Bairro'], helpers.En.bairro)

            # confirmar = page.wait_for_element(Entidade.confirmar)

            # confirmar.click()

            page.driver.execute_script(helpers.En.submit)


def imprime_licenca(page, ident, serv, tipo):

    ident, serv, tipo, sis = functions.check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)


def consultaSigec(page, ident, tipo='cpf'):
    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:
        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:
        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

    page.driver.get(helpers.Sigec.consulta)

    if tipo in ('cpf', 'cnpj'):

        elem = page.wait_for_element_to_click(helpers.Sigec.cpf)

        elem.send_keys(ident + Keys.RETURN)

    elif tipo == 'fistel':

        elem = page.wait_for_element_to_click(helpers.Sigec.fistel)

        elem.send_keys(ident + Keys.RETURN)

    page.wait_for_page_load()

    # TODO: implement other elements
