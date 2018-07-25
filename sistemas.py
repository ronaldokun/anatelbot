import re
from bs4 import  BeautifulSoup as soup
from collections import namedtuple
import functions
import helpers
from page import *
from time import sleep
from selenium.webdriver.common.by import By
import pyperclip as clip # copiar o texto clipboard
import pyautogui as gui


SERVICOS = ["cidadao", "radioamador", "maritimo", "aeronautico", "boleto", "sec"]

PATTERNS = [r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$',
            r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$',
            r'^(P){1}([A-Z]){4}$',
            r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})']

ESTAÇÕES_RC = ["Fixa", "Móvel", "Telecomando"]

STRIP = ("/", ".", "-")

def strip_string(str_):

    return "".join(s for s in str_ if s not in STRIP)


class Sistema(Page):


    def __init__(self, driver, login="", senha="", timeout=5):

        super().__init__(driver)

        self.driver.get('http://sistemasnet')

        self.timeout = timeout

        alert = self.alert_is_present(timeout=timeout)

        if alert:

            alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

            alert.accept()

        return self

    def _navigate(self, identificador: str, tipo_id: str, page_info: tuple, silent=True):
        """ Check id and tipo_id consistency and navigate to link

        :param id: identificador, e.g. cpf: 11 digits, cnpj: 14 digits, indicativo: 4 to 6 characters
        :param tipo_id: cpf, cnpj or indicativo
        :param page_id: tuple (link to page, element id to fill, submit button)
        :return: None
        """
        if not functions.check_input(identificador=identificador, tipo=tipo_id):
            raise ValueError("Identificador deve ser do tipo cpf, cnpj ou indicativo: " % identificador)

        identificador = strip_string(identificador)

        link, _id, submit = page_info

        with self.wait_for_page_load():

            self.driver.get(link)

        self._update_elem(_id, identificador)

        if silent:
            self._click_button(submit)

    def _get_acoes(self, helper, keys):
        return tuple(helper[x] for x in keys)

    def _click_button(self, btn_id, timeout=5):

        try:

            button = self.wait_for_element_to_click(btn_id, timeout=timeout)

            button.click()

        except NoSuchElementException as e:

            print(repr(e))

        alert = self.alert_is_present(timeout=timeout)

        if alert: alert.accept()

    def _update_elem(self, elem_id, dado, timeout=5):

        try:

            elem = self.wait_for_element(elem_id, timeout=timeout)

        except NoSuchElementException as e:

            print(e)

        elem.clear()

        elem.send_keys(dado)

    def _select_by_text(self, select_id, text, timeout=5):

        try:

            select = Select(self.wait_for_element_to_click(select_id))

            select.select_by_visible_text(text)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            alert = self.alert_is_present(timeout=timeout)

            if alert: alert.accept()

            print(repr(e))

    def _extrai_cadastro(self, source):

        #TODO: iterate over the <tbody> tags

        dados = {}

        source = self.driver.page_source

        for tr in source.find_all('tr'):

            for td in tr.find_all('td', string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling('td')

                if value and key not in dados:

                    dados[key] = value.text.strip()

        return dados

class Scpx(Sistema):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Scpx

    def consulta(self, id, tipo_id='id_cpf', timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ('link', tipo_id, 'submit'))

        self._navigate(id, tipo_id, acoes)

        id = strip_string(id)

        try:

            self._click_button((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            pass #print("There is no such element or not found {}".format(id))

        self._click_button(h['id_btn_estacao'], timeout=timeout)

    def imprime_consulta(self, identificador, tipo_id='id_cpf', resumida=False):

        self.consulta(identificador, tipo_id)

        h = self.sis.consulta

        self._click_button(h.get('id_btn_estacao'))

        try:

            if resumida:

                btn_id = h.get('impressao_resumida')


            else:

                btn_id = h.get('impressao_completa')

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return

        self._click_button(btn_id)

    def servico_incluir(self, identificador, num_processo, tipo_id='id_cpf', silent=False):

        h = self.sis.servico

        num_processo = strip_string(num_processo)

        acoes = self._get_acoes(h, ('incluir', tipo_id, 'submit'))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        self._update_elem(h.get('id_num_proc'), num_processo)

        self._click_button(h.get('id_btn_corresp'))

        if silent:
            self._click_button(h.get('submit'))

    def servico_excluir(self, identificador, documento, motivo='Renúncia', tipo_id='id_cpf'):

        h = self.sis.servico

        acoes = self._get_acoes(h, ('excluir', tipo_id, 'submit'))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        alert = self.alert_is_present(2)

        if alert: alert.dismiss()

        self._click_button(h.get('id_btn_dados_exclusão'))

        self._update_elem(h.get('id_doc_exclusão'), documento)

        self._select_by_text(h.get('id_motivo_exclusão'), motivo)

        self._click_button(h.get('submit'))

        alert = self.alert_is_present(2)

        if alert: alert.dismiss()

    def incluir_estacao(self, identificador, tipo_estacao, indicativo, tipo_id='id_cpf', sede=True, sequencial='001',  uf='SP'):

        if tipo_estacao not in ESTAÇÕES_RC:
            raise ValueError("Os tipos de estação devem ser: ".format(ESTAÇÕES_RC))

        assert functions.check_input(indicativo, tipo='indicativo'), 'Formato de Indicativo Inválido'

        helper = self.sis.estacao

        acoes = self._get_acoes(helper, ('incluir', tipo_id, 'submit'))

        self._navigate(identificador, tipo_id, acoes)

        self._click_button(helper.get('id_btn_dados_estacao'))

        self._select_by_text(helper.get('id_uf'), uf)

        alert = self.alert_is_present(5)

        if alert: alert.dismiss()

        self._update_elem(helper.get('id_indicativo'), indicativo)

        self._update_elem(helper.get('id_seq'), sequencial)

        self._select_by_text(helper.get('id_tipo'), tipo_estacao)

        if tipo_estacao == "Fixa" and sede:

            self._click_button(helper.get('copiar_sede'))

        self._click_button(helper.get('submit'), timeout=10)

        alert = self.alert_is_present(2)

        if alert: alert.dismiss()

    def movimento_transferir(self, identificador, origem, dest, proc, tipo_id='id_cpf'):

        helper = self.sis.movimento

        links = ('transferir', tipo_id, 'submit')

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert: alert.accept()

        id_atual = helper.get('id_atual')

        if origem.lower() == "a":

            text = "A - Em análise"

        elif origem.lower() == "b":

            text = "B - Cadastro pela Anatel"

        else:

            print("A transferência de movimento é somente à partir dos Movimentos A ou B")

            return

        self._select_by_text(id_atual, text)

        self._click_button(helper.get('submit'))


        if self.check_element_exists(helper.get('id_proc'), timeout=1):

            proc = re.sub('[.-/]', '', proc)

            self._update_elem(helper.get('id_proc'), proc)

        id_posterior = helper.get('id_posterior')

        if dest.lower() == 'e':

            self._select_by_text(id_posterior, "E - Aprovado / Licença")

        elif dest.lower() == 'g':

            self._select_by_text(id_posterior, "G - Cadastro pelo usuário (auto-cadastramento)")

            self._update_elem(helper.get('id_txt_cancelar'),
                                         "Cadastro Incorreto. Estação será refeita com dados corretos")

        self._click_button(helper.get('submit'))

        alert = self.alert_is_present(5)

        if alert: alert.accept()

    def movimento_cancelar(self, identificador, tipo_id='id_cpf'):

        helper = self.sis.movimento

        links = ('cancelar', tipo_id, 'submit')

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert: alert.accept()

        self._click_button(helper['id_btn_lista_estacoes'])

        self._click_button(helper['id_btn_marcar_todos'])

        self._click_button(helper['submit'])

    def licenciar_estacao(self, identificador, tipo_id='id_cpf', ppdess=True, silent=False):

        helper = self.sis.estacao

        acoes = self._get_acoes(helper, ('licenciar', tipo_id, 'submit'))

        self._navigate(identificador, tipo_id, acoes)

        if tipo_id == 'id_cpf':

            self._click_button((By.LINK_TEXT, strip_string(identificador)))

        if not ppdess:

            self._click_button(helper.get('id_btn_lista_estacoes'))
            self._click_button(helper.get('id_btn_licenciar'))

        if silent:

            alert = self.alert_is_present(5)

            if alert: alert.accept()

    def prorrogar_rf(self, identificador, tipo_id='id_cpf'):

        helper = self.sis.servico

        acoes = self._get_acoes(helper, ('prorrogar_rf', tipo_id, 'submit'))

        self._navigate(identificador,tipo_id, acoes)

        self._click_button(helper.get('id_btn_dados_estacao'))

        self._click_button(helper.get('submit'))

        alert = self.alert_is_present(5)

        if alert: alert.accept()

    def prorrogar_estacao(self, identificador, tipo_id='id_cpf'):

        helper = self.sis.licenca_prorrogar

        acoes = self._get_acoes(helper, ('link', tipo_id, 'submit'))

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException as e:

            print(repr(e))

        alert = self.alert_is_present(timeout=5)

        alert.dismiss()

        self._click_button(helper.get('id_btn_lista_estacoes'))

        self._click_button(helper['submit'])

    def imprimir_licenca(self, identificador, tipo_id="id_cpf"):

        helper = self.sis.licenca['imprimir']

        acoes = self._get_acoes(helper, ('link', tipo_id, 'submit'))

        self._navigate(identificador, helper, acoes)

        self._click_button(helper['id_btn_imprimir'])

    def extrai_cadastro(self, id, tipo_id='id_cpf', timeout=5):

        self.consulta(id, tipo_id, timeout=timeout)

        source = soup(self.driver.page_source, 'lxml')

        return self._extrai_cadastro(source)

class Sec(Sistema):

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Sec

    def _extrai_inscritos_prova(self):

        dados = {}

        source = soup(self.driver.page_source, "lxml")

        base = 'http://sistemasnet/SEC/Prova/BancaEspecialImpressao/'

        Inscrito = namedtuple('Inscrito', 'link cpf nome coer impresso')

        for tr in source.find_all('tr', id=('TRplus2', 'TRplus3', 'TRplus4')):

            td =  list(tr.find_all('td'))

            assert len(td) >= 5, "O identificador tabular retornado não é válido"

            link = td[0].a.attrs['onclick'].split("'")[1]

            link = base + link

            cpf = td[1].label.text.strip()

            nome = td[0].a.text.strip().upper()

            coer = td[2].label.text.strip()

            impresso = hasattr(td[-1].label, 'text') and td[-1].label.text != ""

            dados[cpf] = Inscrito(link, cpf, nome, coer, impresso)

        return dados


    def imprimir_provas(self, data, horario, num_registros, cpf=None):

        h = self.sis.Prova.imprimir

        self.driver.get(h['link'])

        #"http://sistemasnet/SEC/Prova/BancaEspecialImpressao/DadosProva.asp?idtProvaAgenda=11513&NumCpfAvaliador=31888916877")

        if cpf is not None:

            self._update_elem(h['id_cpf'], cpf)

        sleep(2)

        #self._click_button(h['submit'])

        sleep(2)

        #self._click_button((By.LINK_TEXT, " ".join([data, horario])))

        self.driver.execute_script(h['alt_reg'])

        self._update_elem(h['num_reg'], str(num_registros) + Keys.RETURN)

        sleep(5)

        dados = self._extrai_inscritos_prova()

        dados = sorted(list(dados.values()), key=lambda v: v.nome)

        for v in dados:

            self.driver.get(v.link)

            sleep(5)

            clip.copy(v.nome)

            confirm = gui.confirm('Imprimir Prova?')

            if confirm == 'OK':

                self._click_button(h['id_bt_imprimir'])

            else:

                next

            clip.copy(v.nome)

    def alterar_nome(self, cpf, novo):

        pass


class Boleto(Sistema):

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Boleto

    def imprime_boleto(self, ident, tipo_id):
        """ This function receives a webdriver object, navigates it to the
        helpers.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        h = self.sis.imprimir

        # acoes = self._get_acoes(h, ('link', tipo_id, 'submit'))

        self.driver.get(h['link'])

        if tipo_id == 'id_cpf':

            self._click_button(h['id_cpf'])

            input_ = h['input_cpf']

        else:

            self._click_button(h['id_fistel'])

            input_ = h['input_fistel']

        self._update_elem(input_, ident)

        self._update_elem(h['input_data'], functions.last_day_of_month())

        self._click_button(h['submit'])

        self._click_button(h['marcar_todos'])

        self._click_button(h['btn_print'])

        try:

            self.wait_for_new_window()






def save_new_window(page, filename):

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
