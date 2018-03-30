import functions
import helpers
from page import *
from time import sleep

SERVICOS = ["cidadao", "radioamador", "maritimo", "aeronautico", "boleto", "sec"]

PATTERNS = [r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$',
            r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$',
            r'^(P){1}([A-Z]){4}$',
            r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})']

ESTAÇÕES_RC = ["Fixa", "Móvel", "Telecomando"]


class Scpx(Page):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login="", senha=""):

        self.sistema = helpers.Scpx

        self.tipo = 'cpf'

        super().__init__(driver)

    def _navigate(self, identificador, tipo, link, id=None):

        if not id:

            id = self.sistema.Consulta[tipo]

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

                print("The html id: {} is not present on this webpage".format(identificador))

    def consulta(self, identificador, tipo='id_cpf'):

        self._navigate(identificador, tipo, self.sistema.Consulta['link'], self.sistema.Consulta[tipo])

    def imprime_consulta(self, identificador, tipo='id_cpf', resumida=False):

        self.consulta(identificador, tipo)

        try:

            elem = self.wait_for_element_to_click(self.sistema.Consulta['btn_estacao'])

            elem.click()

        except NoSuchElementException:

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

    def incluir_serviço(self, identificador, tipo='id_cpf'):

        self._navigate(identificador, tipo, self.sistema.Servico['incluir'], self.sistema.Consulta[tipo])

        # TODO: Finalizar método

    def incluir_estacao(self, identificador, tipo_estacao, indicativo, sequencial,  tipo='id_cpf', uf='SP'):

        if tipo_estacao not in ESTAÇÕES_RC:
            raise ValueError("Os tipos de estação devem ser: ".format(ESTAÇÕES_RC))

        self._navigate(identificador, tipo, self.sistema.Estacao['incluir'], self.sistema.Consulta[tipo])

        button = self.wait_for_element_to_click(self.sistema.Estacao['id_btn_dados_estacao'])

        button.click()

        try:

            estado = Select(self.wait_for_element(self.sistema.Estacao['id_uf']))

            estado.select_by_value(uf)

        except UnexpectedAlertPresentException as e:

            alert = self.alert_is_present(5)

            if alert:

                alert.dismiss()


        indic= self.wait_for_element(self.sistema.Estacao['id_indicativo'])

        try:

            indic.send_keys(indicativo)

        except UnexpectedAlertPresentException as e:

            alert = self.alert_is_present(2)

            if alert:

                alert.dismiss()

        indic.send_keys(indicativo)

        seq = self.wait_for_element(self.sistema.Estacao["id_seq"])

        seq.send_keys(sequencial)

        tipo_est = Select(self.wait_for_element(self.sistema.Estacao['id_tipo']))

        if tipo_estacao == 'Móvel':

            tipo_est.select_by_visible_text("Móvel")

        elif tipo_estacao == "Fixa":

            tipo_est.select_by_visible_text("Fixa")

        else:
            tipo_est.select_by_visible_text("Telecomando")

        confirmar = self.wait_for_element_to_click(self.sistema.Estacao['id_confirmar'])

        try:

            confirmar.click()

        except UnexpectedAlertPresentException as e:

            alert = self.alert_is_present(2)

            if alert:

                alert.dismiss()

    def aprovar_movimento(self, identificador, origem, tipo='id_cpf'):

        try:
            self._navigate(identificador, tipo, self.sistema.Movimento['transferir'], self.sistema.Consulta[tipo])

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert: alert.accept()


        movimento_atual = Select(self.wait_for_element_to_click(self.sistema.Movimento['atual']))

        if origem.lower() == "a":

            movimento_atual.select_by_visible_text("A - Em Análise")

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['id_confirmar'])

            with self.wait_for_page_load(): confirmar.click()

            movimento_a_transferir = Select(self.wait_for_element_to_click(self.sistema.Movimento['posterior']))

            movimento_a_transferir.select_by_visible_text("")


        elif origem.lower() == "b":

            movimento_atual.select_by_visible_text(("B - Cadastro pela Anatel"))

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['id_confirmar'])

            with self.wait_for_page_load(): confirmar.click()

            movimento_a_transferir = Select(self.wait_for_element_to_click(self.sistema.Movimento['posterior']))

            movimento_a_transferir.select_by_visible_text("E - Aprovado / Licença")

            confirmar = self.wait_for_element_to_click(self.sistema.Estacao['id_confirmar'])

            confirmar.click()

            try:

                alert = self.alert_is_present(5)

                if alert:
                    alert.accept()

            except UnexpectedAlertPresentException:

                pass

    def licenciar_estacao(self, identificador, tipo='id_cpf', ppdess=True):

        if ppdess:

            self._navigate(identificador, tipo, self.sistema.Estacao['licenciar'])

            if tipo == 'id_cpf':

                cpf = self.wait_for_element_to_click((By.LINK_TEXT, identificador))

                cpf.click()

            try:

                lista_estacoes = self.wait_for_element_to_click(self.sistema.Estacao['id_btn_lista_estacoes'])

                lista_estacoes.click()

                self.wait_for_element_to_click(self.sistema.Estacao['id_btn_licenciar']).click()

            except UnexpectedAlertPresentException as e:

                pass

            
        else:

            self._navigate(identificador, tipo, self.sistema.Estacao['licenciar'])

            if tipo == 'id_cpf':

                cpf = self.wait_for_element_to_click((By.LINK_TEXT, identificador))

                cpf.click()

                return

            #alert.accept()

    def prorrogar_rf(self, identificador, tipo='id_cpf'):

        self._navigate(identificador,tipo, self.sistema.Servico['prorrogar_rf'], self.sistema.Consulta[tipo])

        button = self.wait_for_element_to_click(self.sistema.Servico['id_btn_dados_estacao'])

        button.click()

        confirmar = self.wait_for_element_to_click(self.sistema.Servico['id_confirmar'])

        confirmar.click()

        alert = self.alert_is_present(5)

        if alert:

            alert.accept()

    def prorrogar_estacao(self, identificador, tipo='id_cpf'):

        self._navigate(identificador,tipo, self.sistema.Licenca['prorrogar'])

        button = self.wait_for_element_to_click(self.sistema.Licenca['id_btn_lista_estacoes'])

        button.click()

    def imprimir_licenca(self, identificador, tipo="id_cpf"):

        self._navigate(identificador, tipo=tipo, link=self.sistema.Licenca["imprimir"], id=self.sistema.Licenca['cpf'])







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

    cpf = page.wait_for_element_to_click(helpers.Entidade.idade.cpf)

    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)

    if 'Email' in dados:
        atualiza_campo(dados['Email'], helpers.Entidade.idade.email)

    btn = page.wait_for_element_to_click(helpers.Entidade.idade.bt_dados)

    btn.click()

    if 'RG' in dados:
        atualiza_campo(dados['RG'], helpers.Entidade.idade.rg)

    if 'Orgexp' in dados:
        atualiza_campo(dados['Orgexp'], helpers.Entidade.idade.orgexp)

    if 'Data de Nascimento' in dados:
        data = dados['Data de Nascimento']

        data = data.replace('-', '')

        atualiza_campo(data, helpers.Entidade.nasc)

    btn = page.wait_for_element_to_click(helpers.Entidade.bt_fone)

    btn.click()

    if 'ddd' in dados:

        atualiza_campo(dados['ddd'], helpers.Entidade.ddd)

    else:

        ddd = '11'

        atualiza_campo(ddd, helpers.Entidade.ddd)

        # if 'Fone' in dados:

    #   atualiza_campo(dados['Fone'], Entidade.fone)

    # else:

    #   fone = '123456789'

    #  atualiza_campo(fone, Entidade.fone)

    btn = page.wait_for_element_to_click(helpers.Entidade.bt_end)

    btn.click()

    if 'Cep' in dados:

        cep = dados['Cep']

        cep = cep.replace('-', '')

        atualiza_campo(cep, helpers.Entidade.cep)

        cep = page.wait_for_element_to_click(helpers.Entidade.bt_cep)

        cep.click()

        for i in range(30):

            logr = page.wait_for_element(helpers.Entidade.logr)

            if logr.get_attribute('value'):
                break

            sleep(1)

        else:

            if 'Logradouro' not in dados:
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], helpers.Entidade.logr)

        if 'Número' not in dados:

            raise ValueError("É obrigatório informar o número na atualização\
            do endereço")

        else:

            atualiza_campo(dados['Número'], helpers.Entidade.num)

            if 'Complemento' in dados:
                atualiza_campo(dados['Complemento'], helpers.Entidade.comp)

            bairro = page.wait_for_element(helpers.Entidade.bairro)

            if not bairro.get_attribute('value'):

                if 'Bairro' not in dados:
                    raise ValueError("É obrigatório informar o bairro na atualização\
                                     do endereço")

            else:

                atualiza_campo(dados['Bairro'], helpers.Entidade.bairro)

            # confirmar = page.wait_for_element(Entidade.confirmar)

            # confirmar.click()

            page.driver.execute_script(helpers.Entidade.submit)


def imprime_licenca(page, ident, serv, tipo):

    ident, serv, tipo, sis = functions.check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)


def consultaSigec(page, ident, tipo='id_cpf'):
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
