import re
from bs4 import  BeautifulSoup as soup
from collections import namedtuple, defaultdict
import functions
import helpers
from page import *
from time import sleep
from selenium.webdriver.common.by import By
import pyperclip as clip # copiar o texto clipboard
import pyautogui as gui


SERVICOS = ["cidadao", "radioamador", "maritimo", "aeronautico", "boleto", "sec"]

PATTERNS = [r'^(P){1}(X){1}(\d){1}([A-Z]){1}(\d){4}$',
            r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$',
            r'^(P){1}([A-Z]){4}$',
            r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})']

ESTAÇÕES_RC = ["Fixa", "Móvel", "Telecomando"]

SEC_DADOS = {'Dados do Usuário': ["E-mail"],
             'Dados Complementares': ["Identidade", "Órgão Exp.", "Sexo", "Estado Civil",
                                      "Data de Nascimento", "Núm. CREA", "Sigla UF CREA"],
             "Telefones": ["DDD", "Fone"],
             'Endereço': ["Endereço", "Número", "Complemento", "Bairro", "Município", "UF", "Cep"]}

STRIP = ("/", ".", "-")

def strip_string(str_):

    return "".join(s for s in str_ if s not in STRIP)


class Sistema(Page):

    def __init__(self, driver, login=None, senha=None, timeout=5):

        if login and senha:

            self.driver = functions.init_browser(driver, login, senha, timeout)

        else:

            self.driver = driver

    def _navigate(self, identificador: str, tipo_id: str, acoes: tuple, silent=True):
        """ Check id and tipo_id consistency and navigate to link

        :param id: identificador, e.g. cpf: 11 digits, cnpj: 14 digits, indicativo: 4 to 6 characters
        :param tipo_id: cpf, cnpj or indicativo
        :param page_id: tuple (link to page, element id to fill, submit button)
        :return: None
        """
        if not functions.check_input(identificador=identificador, tipo=tipo_id):
            raise ValueError("Identificador deve ser do tipo cpf, cnpj ou indicativo: " % identificador)

        identificador = strip_string(identificador)

        link, _id, submit = acoes

        with self.wait_for_page_load():

            self.driver.get(link)

        if silent:

            if not submit:

                self._update_elem(_id, identificador+Keys.RETURN)

            else:

                self._update_elem(_id, identificador)

                return self._click_button(submit)

        else:

            self._update_elem(_id, identificador)

    def _get_acoes(self, helper, keys):
        return tuple(helper.get(x, None) for x in keys)

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

        acoes = self._get_acoes(h, ('link', tipo_id, None)) #'submit'))

        self._navigate(id, tipo_id, acoes)

        id = strip_string(id)

        try:

            self._click_button((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não há mais de um registro de Outorga")

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

        dados = {}

        source = soup(self.driver.page_source, 'lxml')

        for tr in source.find_all('tr'):

            for td in tr.find_all('td', string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling('td')

                if key not in dados and hasattr(value, 'text'):
                    dados[key] = value.text.strip()

        return dados

class Scra(Sistema):
    """
        Esta subclasse da classe Page define métodos de execução de funções nos sistemas
        interativos da ANATEL
        """

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Scra

    def consulta(self, id, tipo_id='id_cpf', timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ('link', tipo_id, None))  # 'submit'))

        self._navigate(id, tipo_id, acoes)

        id = strip_string(id)

        try:

            self._click_button((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            pass  # print("There is no such element or not found {}".format(id))

        self._click_button(h['id_btn_estacao'], timeout=timeout)

    def imprimir_licenca(self, id, tipo_id="id_cpf", timeout=5):

        helper = self.sis.licenca['imprimir']

        acoes = self._get_acoes(helper, ('link', tipo_id, 'submit'))

        self._navigate(id, helper, acoes)

        id = strip_string(id)

        try:

            self._click_button((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não foi possível navegar para a página de consulta")


        self._click_button(helper['id_btn_imprimir'])

    def extrai_cadastro(self, id, tipo_id='id_cpf', timeout=5):

        self.consulta(id, tipo_id, timeout=timeout)

        dados = {}

        source = soup(self.driver.page_source, 'lxml')

        for tr in source.find_all('tr'):

            for td in tr.find_all('td', string=True):

                key = td.text.strip(" :")

                value = td.find_next_sibling('td')

                if not hasattr(value, 'text'): next

                if key not in dados and value:
                    dados[key] = value.text.strip()

        return dados

class Sec(Sistema):

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Sec

    def consulta(self, id, tipo_id='id_cpf', timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ('link', tipo_id, 'submit')) #'submit'))

        self._navigate(id, tipo_id, acoes)

        id = strip_string(id)

        try:

            self._click_button((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            pass

    def atualiza_cadastro(self, dados, novo=False):

        """

        :param dados: dictionary of all the fiels in the Sec -> Entidade -> Alterar page
        :return: None

        It assumes all values are correctly pre-formatted
        """

        #TODO: generalize and check_input

        h = self.sis.entidade

        cpf = dados['CPF'].replace("-", "").replace(".", "")

        while len(cpf) < 11:

            cpf = '0' + cpf

        acoes = self._get_acoes(h, ('alterar', 'id_cpf', 'submit'))

        if not self._navigate(cpf, h, acoes):

            acoes = self._get_acoes(h, ('incluir', 'id_cpf', 'submit'))

            self._navigate(cpf, h, acoes)

            #nome = self.wait_for_element_to_be_visible(h['input_nome'])

            #nome.send_keys(dados['Nome'])

            self._update_elem(h['input_nome'], dados["Nome"])


        for key in SEC_DADOS['Dados do Usuário']:

            value = dados.get(key, "")

            if value != "":
                self._update_elem(h[key], value)

        self._click_button(h['bt_dados'])

        for key in SEC_DADOS['Dados Complementares']:

            value = dados.get(key, "")

            if value != "":
                self._update_elem(h[key], value)

        self._click_button(h['bt_fone'])

        for key in SEC_DADOS['Telefones']:

            value = dados.get(key, "")

            if value != "":

                self._update_elem(h[key], value)

        self._click_button(h['bt_end'])

        cep = dados.get('Cep', "").replace("-", '')

        if cep != "":

            self._update_elem(h['Cep'], cep)

            self._click_button(h['bt_cep'])

            alert = self.alert_is_present(5)

            if alert:

                return(alert.get_text)

            uf = self.wait_for_element_to_be_visible(h['UF'])

            # After clicking the 'bt_cep' button it takes a while until the uf.value attribute is set
            # until then there is no uf.value
            while not uf.get_attribute('value'):

                uf = self.wait_for_element_to_be_visible(h['UF'])

            logr = self.wait_for_element_to_be_visible(h['Endereço'])

            # if the CEP loading didn't retrieve the logradouro, update it manually
            if not logr.get_attribute('value'):

                self._update_elem(h['Endereço'], dados['Endereço'].title())

            bairro = self.wait_for_element(h['Bairro'])

            if not bairro.get_attribute('value'):

                self._update_elem(h['Bairro'], dados["Bairro"].title())

            if 'Número' not in dados:
                raise ValueError("É obrigatório informar o número do endereço")

            self._update_elem(h['Número'], dados['Número'])

            comp = dados.get("Complemento", "").title()

            self._update_elem(h['Complemento'], comp)

        #self.driver.execute_script(h['submit_script'])

        self._click_button(h['submit'])

        alert = self.alert_is_present(30)

        if alert:

            return alert.accept()

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

    def inscrever_candidato(self, cpf, uf, certificado, data):

        h = self.sis.inscricao['incluir']

        # self.driver.get("http://sistemasnet/SEC/Chamada/CadastroSRFRegularizado.asp")
        #
        # self._update_elem((By.ID, "NumCNPJCPF"), cpf)
        #
        # self._click_button(h['submit'])
        #
        # try:
        #
        #     self._select_by_text((By.ID, "CodSituacaoCadastralNova"), "Regular")
        #
        #     self._click_button(h['submit'])
        #
        # except:
        #
        #     pass
        #
        # h = self.sis.inscricao['incluir']

        self.driver.get(h['link'])

        self._update_elem(h['id_cpf'], cpf)

        self._select_by_text(h['id_uf'], uf)

        self._select_by_text(h['id_certificado'], certificado)

        self._click_button(h['submit'])

        sleep(1)

        self._click_button((By.LINK_TEXT, data))

        alert = self.alert_is_present(timeout=10)

        alert.accept()

        sleep(1)





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

    def extrai_cadastro(self, id, tipo_id='id_cpf', timeout=5):

        self.consulta(id, tipo_id, timeout=timeout)

        self.wait_for_element_to_be_visible((By.ID, 'divusuario'), timeout=timeout)

        dados = {}

        source = soup(self.driver.page_source, 'lxml')

        for tr in source.find_all('tr'):

            for td in tr.find_all('td', string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling('td')

                # TODO: Adaptar para tabulação referente às provas
                if key not in dados and hasattr(value, 'text'):
                    dados[key] = value.text.strip()

        return dados

    def alterar_nome(self, cpf, novo):

        pass

class Sigec(Sistema):


    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Sigec

    def extrai_cadastro(self, id, tipo_id='id_cpf'):

        self.consulta_geral(id, tipo_id, 30)

        dados = {}

        source = soup(self.driver.page_source, 'lxml')

        for tr in source.find_all('tr'):

            for td in tr.find_all('td', string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling('td')

                if key not in dados:
                    dados[key] = value.text.strip()

        return dados
    def consulta_geral(self, ident, tipo_id='id_cpf', timeout=5, simples=True):

        h = self.sis.consulta['geral']

        acoes = self._get_acoes(h, ('link', tipo_id, 'submit'))

        if not simples:
            pass

        self._navigate(ident, tipo_id, acoes)

class Boleto(Sistema):


    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = helpers.Boleto
    def imprime_boleto(self, ident, tipo_id):

        """ This function receives a webdriver object, navigates it to the
        helpers.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        # acoes = self._get_acoes(h, ('link', tipo_id, 'submit'))

        h = self.sis.imprimir

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

def imprime_licenca(page, ident, serv, tipo):

    ident, serv, tipo, sis = functions.check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)

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
