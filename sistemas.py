import functions
import helpers
from page import *
from time import sleep
from selenium.webdriver.common.by import By




from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities

SERVICOS = ["cidadao", "radioamador", "maritimo", "aeronautico", "boleto", "sec"]

PATTERNS = [r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$',
            r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$',
            r'^(P){1}([A-Z]){4}$',
            r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})']

ESTAÇÕES_RC = ["Fixa", "Móvel", "Telecomando"]


class Sistema(Page):

    def __init__(self, driver, login="", senha="", timeout=5):

        super().__init__(driver)

        self.driver.get('http://sistemasnet')

        alert = self.alert_is_present(timeout=timeout)

        if alert:

            alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

            alert.accept()

        return self

    def get_dados_navegacao(dict_acao, tipo):

        if not link:

            link = dict_acao.get('link')

        if not id_:

            id_ = dict_acao.get(tipo)

        if not submit:

            submit = dict_acao.get('id_confirmar')

        return (link, id_, submit)

    def _navigate(self, identificador: str, tipo_id: str, page_info: tuple):
        """ Check id and tipo_id consistency and navigate to link

        :param id: identificador, e.g. cpf: 11 digits, cnpj: 14 digits, indicativo: 4 to 6 characters
        :param tipo_id: cpf, cnpj or indicativo
        :param page_id: tuple (link to page, element id to fill, submit button)
        :return: None
        """
        if not functions.check_input(identificador=identificador, tipo=tipo_id):
            raise ValueError("Identificador deve ser do tipo cpf, cnpj ou indicativo: " % identificador)

        link, _id, submit = page_info

        with self.wait_for_page_load():

            self.driver.get(link)

        with self.wait_for_page_load():

            try:

                elem = self.wait_for_element_to_click(_id, timeout=10)

                elem.send_keys(identificador) # + Keys.RETURN)

            except NoSuchElementException:

                print("The html id: {} is not present on this webpage".format(_id))

            try:

                submit = self.wait_for_element_to_click(submit, timeout=2)

                submit.click()

            except (NoSuchElementException, TimeoutException):

                print("Não foi possível clicar no Botão Confirmar")


class Scpx(Sistema):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login="", senha="", timeout=5):

        super().__init__(driver, login, senha, timeout)

        self.sistema = helpers.Scpx

    def _get_acoes(self, helper, keys):
        return tuple(helper.get(x) for x in keys)

    def consulta(self, id, tipo_id='id_cpf'):

        helper = self.sistema.Consulta

        links = ('link', tipo_id, 'submit')

        acoes = self._get_acoes(helper, links)

        self._navigate(id, tipo_id, acoes)

        try:

            self.wait_for_element_to_click((By.LINK_TEXT, id), timeout=5).click()

        except (NoSuchElementException, TimeoutException):

            pass

    def imprime_consulta(self, identificador, tipo_id='id_cpf', resumida=False):

        self.consulta(identificador, tipo_id)

        try:

            elem = self.wait_for_element_to_click(self.sistema.Consulta['id_btn_estacao'])

            elem.click()

        except NoSuchElementException:

            print("Não foi possível clicar no botão 'Estação' na página consulta")

            return

        try:

            if resumida:

                # self.driver.execute_script("VersaoImpressao('R')")
                btn = self.wait_for_element_to_click(self.sistema.Consulta.get('impressao_resumida'))


            else:

                # self.driver.execute_script("VersaoImpressao('N')")
                btn = self.wait_for_element_to_click(self.sistema.Consulta.get('impressao_completa'))

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return

        #windows = self.driver.window_handles

        #main = windows[-1]

        btn.click()

        #self.wait_for_new_window(windows)

        # windows = self.driver.window_handles
        #
        # self.driver.switch_to_window(windows[-1])
        #
        # print(self.get_title())
        #
        # self.driver.switch_to_frame(self.sistema.Consulta.get('frame_impressao'))
        #
        # try:
        #
        #     imprimir = self.wait_for_element_to_be_visible(self.sistema.Consulta.get('imprimir'))
        #
        #     imprimir.click()
        #
        #
        # except (NoSuchElementException, TimeoutException):
        #
        #     print("Não foi possível imprimir a página de consulta")
        #
        # finally:
        #
        #     #self.close()
        #
        #     self.driver.switch_to_window(main)

    def servico_incluir(self, identificador, tipo_id='id_cpf'):

        helper = self.sistema.Servico

        acoes = self._get_acoes(helper, ('incluir', tipo_id, 'submit'))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")


    def servico_excluir(self, identificador, documento, motivo='Renúncia', tipo_id='id_cpf'):

        helper = self.sistema.Servico

        acoes = self._get_acoes(helper, ('excluir', tipo_id, 'submit'))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        alert = self.alert_is_present(2)

        if alert: alert.dismiss()

        btn = self.wait_for_element_to_click(helper['id_btn_dados_exclusão'])

        btn.click()

        doc = self.wait_for_element_to_be_visible(helper.get('id_doc_exclusão'))

        doc.send_keys(documento)

        motive = Select(self.wait_for_element_to_be_visible(helper.get('id_motivo_exclusão')))

        motive.select_by_visible_text(motivo)

        confirmar = self.wait_for_element_to_click(helper['submit'])

        confirmar.click()

        alert = self.alert_is_present(2)

        if alert: alert.dismiss()

    def incluir_estacao(self, identificador, tipo_estacao, indicativo, sede=True, sequencial='001', tipo_id='id_cpf', uf='SP'):

        if tipo_estacao not in ESTAÇÕES_RC:
            raise ValueError("Os tipos de estação devem ser: ".format(ESTAÇÕES_RC))

        helper = self.sistema.Estacao

        acoes = tuple([helper.get(x) for x in ('incluir', tipo_id, 'submit')])

        self._navigate(identificador, tipo_id, acoes)

        button = self.wait_for_element_to_click(helper['id_btn_dados_estacao'])

        button.click()

        estado = Select(self.wait_for_element(helper['id_uf']))

        estado.select_by_value(uf)

        alert = self.alert_is_present(5)

        if alert:

            alert.dismiss()

        indic= self.wait_for_element(helper['id_indicativo'])

        try:

            indic.send_keys(indicativo)

        except UnexpectedAlertPresentException as e:

            alert = self.alert_is_present(2)

            if alert:

                alert.dismiss()

        indic.send_keys(indicativo)

        seq = self.wait_for_element(helper["id_seq"])

        seq.send_keys(sequencial)

        tipo_est = Select(self.wait_for_element(helper['id_tipo']))

        if tipo_estacao == 'Móvel':

            tipo_est.select_by_visible_text("Móvel")

        elif tipo_estacao == "Fixa":

            tipo_est.select_by_visible_text("Fixa")

            if sede:

                btn_sede = self.wait_for_element_to_click(helper['copiar_sede'])

                btn_sede.click()

        else:

            tipo_est.select_by_visible_text("Telecomando")

        if sede:

            confirmar = self.wait_for_element_to_click(helper['submit'])

            confirmar.click()

            alert = self.alert_is_present(2)

            if alert: alert.dismiss()

    def movimento_aprovar(self, identificador, origem, tipo_id='id_cpf'):

        helper = self.sistema.Movimento

        links = ('transferir', tipo_id, 'submit')

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert: alert.accept()


        movimento_atual = Select(self.wait_for_element_to_click(helper['atual']))

        if origem.lower() == "a":

            movimento_atual.select_by_visible_text("A - Em análise")

        elif origem.lower() == "b":

            movimento_atual.select_by_visible_text(("B - Cadastro pela Anatel"))

        else:

            print("A transferência de movimento é somente à partir dos Movimentos A ou B")

        confirmar = self.wait_for_element_to_click(helper['submit'])

        with self.wait_for_page_load(): confirmar.click()

        movimento_a_transferir = Select(self.wait_for_element_to_click(helper['posterior']))

        movimento_a_transferir.select_by_visible_text("E - Aprovado / Licença")

        confirmar = self.wait_for_element_to_click(helper['submit'])

        confirmar.click()

        alert = self.alert_is_present(5)

        if alert: alert.accept()

    def licenciar_estacao(self, identificador, tipo_id='id_cpf', ppdess=True):

        helper = self.sistema.Estacao

        acoes = tuple([helper.get(x) for x in ('licenciar', tipo_id, 'submit')])


        self._navigate(identificador, tipo_id, acoes)

        if tipo_id == 'id_cpf':

            cpf = self.wait_for_element_to_click((By.LINK_TEXT, identificador))

            cpf.click()

        if not ppdess:

            lista_estacoes = self.wait_for_element_to_click(helper['id_btn_lista_estacoes'])

            lista_estacoes.click()

            self.wait_for_element_to_click(helper['id_btn_licenciar']).click()

        # Confirma o primeiro licenciamento

        # alert = self.alert_is_present(5)

        # if alert = alert.accept()

    def prorrogar_rf(self, identificador, tipo='id_cpf'):

        helper = self.sistema.Servico

        acoes = tuple([helper.get(x) for x in ('prorrogar', tipo_id, 'submit')])

        self._navigate(identificador,tipo_id, acoes)

        button = self.wait_for_element_to_click(helper['id_btn_dados_estacao'])

        button.click()

        confirmar = self.wait_for_element_to_click(helper['id_confirmar'])

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


    # TODO: implement other elements

def abrir_agenda_prova(sec, datas):

    for data in datas:
        sec.driver.get(helpers.Sec.Agenda_Incl)

        elem = sec.wait_for_element_to_click(helpers.Agenda.data)
        elem.send_keys(data[0])

        elem = sec.wait_for_element_to_click(helpers.Agenda.hora)
        elem.send_keys(data[1])

        elem = sec.wait_for_element_to_click(helpers.Agenda.avaliador)
        elem.send_keys("31888916877")

        elem = sec.wait_for_element_to_click(helpers.Agenda.local)
        elem.send_keys("ANATEL SP. Proibido Bermuda e Regata")

        elem = sec.wait_for_element_to_click(helpers.Agenda.ddd)
        elem.send_keys("11")

        elem = sec.wait_for_element_to_click(helpers.Agenda.fone)
        elem.send_keys("Somente pelo Fale Conosco em www.anatel.gov.br")

        elem = sec.wait_for_element_to_click(helpers.Agenda.responsavel)
        elem.send_keys("Ronaldo S.A. Batista")

        elem = sec.wait_for_element_to_click(helpers.Agenda.vagas)
        elem.send_keys("4")

        elem = sec.wait_for_element_to_click(helpers.Agenda.morse)
        elem.click()

        elem = sec.wait_for_element_to_click(helpers.Agenda.pc)
        elem.click()

        elem = sec.wait_for_element_to_click(helpers.Agenda.dias)
        elem.send_keys("1")

        elem = sec.wait_for_element_to_click(helpers.Agenda.btn_endereco)
        elem.click()

        sleep(1)

        elem = sec.wait_for_element_to_click(helpers.Agenda.cep)
        elem.send_keys("04101300")

        elem = sec.wait_for_element_to_click(helpers.Agenda.btn_buscar_end)
        elem.click()

        sleep(5)

        elem = sec.wait_for_element_to_click(helpers.Agenda.numero)
        elem.send_keys("3073")

        elem = sec.wait_for_element_to_click(helpers.Agenda.btn_certificado)
        elem.click()

        sleep(1)

        elem = Select(sec.wait_for_element_to_click(helpers.Agenda.select_cert_1))
        elem.select_by_visible_text("Certificado de Operador de Estação de Radioamador-Classe A")

        sec.driver.execute_script("AdicionarCertificado('');")
        sleep(1)

        elem = Select(sec.wait_for_element_to_click(helpers.Agenda.select_cert_2))
        elem.select_by_visible_text("Certificado de Operador de Estação de Radioamador-Classe C")

        elem = sec.wait_for_element_to_click(helpers.Agenda.btn_confirmar)
        elem.click()

        try:

            alert = sec.alert_is_present(5)

            sleep(2)

            alert.accept()

        except TimeoutException:

            print("Não foi possível aceitar o alerta")
