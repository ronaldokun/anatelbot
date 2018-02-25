# modules only
import re

import unidecode

from page import *
from page.page import Page
from sei import _functions
from sei import _locators

SERVICOS = ('Outorga: Rádio do Cidadão',
             'Outorga: Radioamador',
             'Outorga: Limitado Móvel Aeronáutico',
             'Outorga: Limitado Móvel Marítimo')


def login_sei(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    browser = Page(driver)
    browser.driver.get(_locators.Login.URL)
    # page.driver.maximize_window()

    usuario = browser.wait_for_element_to_click(_locators.Login.LOG)
    senha = browser.wait_for_element_to_click(_locators.Login.PWD)

    # Clear any clutter on the form
    usuario.clear()
    usuario.send_keys(usr)

    senha.clear()
    senha.send_keys(pwd)

    # Hit Enter
    senha.send_keys(Keys.RETURN)

    return Sei(browser.driver)


class Sei(Page):
    """
    Esta subclasse da classe Page define métodos de execução de ações na
    página principal do SEI e de resgate de informações
    """

    def __init__(self, driver):
        super().__init__(driver)
        self._processos = {}

    def go(self, link):
        """ Simplifies the navigation of href pages on sei.anatel.gov.br
        by pre-appending the required prefix NAV_URL
       """
        link = _locators.Base.URL + link

        self.driver.get(link)

    def get_processos(self):
        return self._processos

    def _set_processos(self, processos):
        self._processos = {p['numero']: p for p in processos}

    def filter_processos(self, processos, servicos=SERVICOS):
        self._processos = {k: v for k, v in processos.items() if v.get('tipo') in servicos}

    def create_processo(self, num, tags=None):
        return Processo(self.driver, num, tags)

    def see_detailed(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.wait_for_element_to_click(_locators.Main.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                _locators.Main.VISUAL)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def is_init_page(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == _locators.Main.TITLE

    def go_to_init_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        self.wait_for_element_to_click(
            _locators.Base.INIT).click()

    def show_lat_menu(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(_locators.Base.MENU)

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()

    def itera_processos(self):
        """
        Navega as páginas de processos abertos no SEI e guarda as tags
        html dos processos como objeto soup no atributo processos_abertos
        """

        # Apaga o conteúdo atual da lista de processos
        processos = []

        # assegura que está inicial
        if not self.is_init_page():
            self.go_to_init_page()

        # Mostra página com informações detalhadas
        self.see_detailed()

        contador = Select(self.wait_for_element(_locators.Main.CONT))

        paginas = [pag.text for pag in contador.options]

        for pag in paginas:
            # One simple repetition to avoid more complex code
            contador = Select(self.wait_for_element(_locators.Main.CONT))
            contador.select_by_visible_text(pag)
            html_sei = Soup(self.driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        processos = [_functions.armazena_tags(
            [tag for tag in line.contents if tag != '\n'])
            for line in processos]

        self._set_processos(processos)

    def update_elem(self, elem_id, dado):

        elem = self.wait_for_element(elem_id)

        elem.clear()

        elem.send_keys(dado)

    # noinspection PyProtectedMember
    def see_contacts(self, nome):

        nome = unidecode._unidecode(nome)

        if self.get_title() != _locators.Contato.TITLE:
            self.go_to_contact_page()

        contato = self.wait_for_element_to_click(_locators.Tipos.CONTATO)

        contato.clear()

        contato.send_keys(nome + Keys.RETURN)

        self.wait_for_page_load()

        # if not self.elem_is_visible((By.LINK_TEXT, "Nenhum Registro Encontrado")):

        self.wait_for_element_to_be_visible((By.XPATH, "//*[contains(text(), nome)]"))

        html = Soup(self.driver.page_source, 'lxml')

        tags = html.find_all('tr', class_='infraTrClara')

        return (len(tags), tags) if tags else (0, None)

    def update_contacts(self, link, dados):

        self.go(link)

        tipo = Select(self.wait_for_element_to_be_visible(_locators.Contato.TIPO))

        tipo.select_by_visible_text("Pessoa Física")

        self.wait_for_element_to_click(_locators.Contato.PF).click()

        self.update_elem(_locators.Contato.SIGLA, dados['CPF'])

        if dados['SEXO'] == 'MASCULINO':

            self.wait_for_element_to_click(_locators.Contato.MASCULINO).click()

        elif dados['SEXO'] == 'FEMININO':

            self.wait_for_element_to_click(_locators.Contato.FEMININO).click()

        self.update_elem(_locators.Contato.NOME, dados['NOME'])

        self.update_elem(_locators.Contato.END, dados['ENDERECO'] + ' ' + dados['NUM'])

        self.update_elem(_locators.Contato.COMP, dados['COMP'])

        self.update_elem(_locators.Contato.BAIRRO, dados['BAIRRO'])

        uf = Select(self.wait_for_element(_locators.Contato.UF))

        uf.select_by_visible_text(dados['UF'])

        cidade = Select(self.wait_for_element_to_be_visible(_locators.Contato.CIDADE))

        cidade.select_by_visible_text(dados["CIDADE"])

        self.update_elem(_locators.Contato.CEP, dados['CEP'])

        self.update_elem(_locators.Contato.CPF, dados['CPF'])

        self.update_elem(_locators.Contato.RG, dados['RG'])

        self.update_elem(_locators.Contato.ORG, dados['ORG'])

        self.update_elem(_locators.Contato.NASC, dados['NASC'])

        self.update_elem(_locators.Contato.FONE, dados['FONE'])

        self.update_elem(_locators.Contato.CEL, dados['CEL'])

        self.update_elem(_locators.Contato.EMAIL, dados['EMAIL'])

        self.wait_for_element_to_click(_locators.Contato.SALVAR).click()

    def go_to_contact_page(self):

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find('li', string='Listar')

        if not tag:
            raise LookupError("The tag of type {0} and string {1} is not present in the page".format('<li>', 'Listar'))

        link = tag.a.attrs['href']

        self.go(link)

    def cria_processo(self, tipo, desc='', inter='', nivel='público'):

        tipo = str(tipo)

        assert tipo in _locators.Tipos.PROCS, \
            print("O tipo de processo digitado {0}, não é válido".format(str(tipo)))

        self.show_lat_menu()

        init_proc = self.wait_for_element_to_click(_locators.Menu.INIT_PROC)

        init_proc.click()

        filtro = self.wait_for_element_to_click(_locators.Tipos.FILTRO)

        filtro.send_keys(tipo)

        # exibe_todos = Sei.wait_for_element_to_click(loc.Tipos.EXIBE_ALL)

        # exibe_todos.click()

        # select = Select(Sei.wait_for_element(loc.Tipos.SL_TIP_PROC))

        tipo = self.wait_for_element_to_click((By.LINK_TEXT, tipo))

        tipo.click()

        if desc:
            espec = self.wait_for_element(_locators.Processo.ESPEC)

            espec.send_keys(desc)

        if inter:
            self.cadastrar_interessado(inter)
            self.consultar_contato(inter)

        if nivel == 'público':

            nivel = self.wait_for_element(_locators.Processo.PUBL)

        elif nivel == 'restrito':

            nivel = self.wait_for_element(_locators.Processo.REST)

        else:

            nivel = self.wait_for_element(_locators.Processo.SIG)

        nivel.click()


class Processo(Sei):

    def __init__(self, driver, numero, tags=None):
        super().__init__(driver)
        self.numero = numero
        self.tags = tags
        self.tree = {}

    def get_tags(self):
        return self.tags

    def close_processo(self):
        self.driver.close()

    def info_oficio(self, num_doc):
        assert self.get_title() == _locators.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to tree frame
        self.driver.switch_to_frame("ifrArvore")

        with self.wait_for_page_load():
            html_tree = Soup(self.driver.page_source, "lxml")

            info = html_tree.find(title=re.compile(num_doc)).string

            assert info != '', "Falha ao retornar Info do Ofício da Árvore"

            # return to parent frame
            self.driver.switch_to_default_content()

            return info

    def actions_oficio(self):
        assert self.get_title() == _locators.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to central frame
        self.driver.switch_to_frame("ifrVisualizacao")

        self.wait_for_element(_locators.Central.ACOES)

        html_frame = Soup(self.driver.page_source, "lxml")

        buttons = html_frame.find(id="divArvoreAcoes").contents

        self.driver.switch_to_default_content()

        return buttons

    def update_andamento(self, buttons, info):
        assert self.get_title() == _locators.Processo.TITLE, \
            "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = _locators.Base.URL + andamento.attrs['href']

        (proc_window, and_window) = Page.nav_link_to_new_win(self.driver, link)

        input_and = self.wait_for_element(_locators.Central.IN_AND)

        text = _locators.Central.AND_PRE + info + _locators.Central.AND_POS

        input_and.send_keys(text)

        self.wait_for_element_to_click(_locators.Central.SV_AND).click()

        self.driver.close()

        self.driver.switch_to_window(proc_window)

    def send_proc_to_sede(self, buttons):
        with self.wait_for_page_load():
            assert self.get_title() == _locators.Processo.TITLE, \
                "Erro na função 'send_proc_to_sede"

            enviar = buttons[3]

            link = _locators.Base.URL + enviar.attrs["href"]

            (janela_processo, janela_enviar) = Page.nav_link_to_new_win(
                self.driver, link)

        with self.wait_for_page_load():
            assert self.get_title() == _locators.Envio.TITLE, \
                "Erro ao clicar no botão 'Enviar Processo'"

            self.driver.execute_script(_locators.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.driver.switch_to_window(janela_unidades)

        assert self.get_title() == _locators.Envio.UNIDS, \
            "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.wait_for_element(_locators.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(_locators.Envio.SIGLA + Keys.RETURN)

        sede = self.wait_for_element(_locators.Envio.ID_SEDE)

        assert sede.get_attribute("title") == _locators.Envio.SEDE, \
            "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.wait_for_element_to_click(_locators.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.driver.close()

        # Troca o foco do navegador
        self.driver.switch_to_window(janela_enviar)

        self.wait_for_element_to_click(_locators.Envio.OPEN).click()

        self.wait_for_element_to_click(_locators.Envio.RET_DIAS).click()

        prazo = self.wait_for_element(_locators.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(_locators.Envio.PRAZO)

        self.wait_for_element_to_click(_locators.Envio.UTEIS).click()

        self.wait_for_element_to_click(_locators.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.driver.close()

        self.driver.switch_to_window(janela_processo)

    def expedir_oficio(self, num_doc):

        info = self.info_oficio(num_doc)

        buttons = self.actions_oficio()

        self.update_andamento(buttons, info)

        self.send_proc_to_sede(buttons)

    def clean_marcadores(self):

        if self.tags.get('anotacao'):

            link = self.tags.get('anotacao_link')

            (main, new) = Page.nav_link_to_new_win(self.driver, link)

            postit = self.wait_for_element(_locators.Central.IN_POSTIT)

            postit.clear()

            btn = self.wait_for_element_to_click(_locators.Central.BT_POSTIT)

            btn.click()

            self.close()

            self.driver.switch_to_window(main)

            self.tags['anotacao'] = ''

def exibir_bloco(Sei, numero):
    if Sei.get_title() != loc.Blocos.TITLE:
        Sei.go_to_blocos()

    try:
        Sei.wait_for_element((By.LINK_TEXT, str(numero))).click()

    except:
        print("O Bloco de Assinatura informado não existe ou está \
              concluído!")


def armazena_bloco(Sei, numero):
    if Sei.get_title() != loc.Bloco.TITLE + " " + str(numero):
        Sei.exibir_bloco(numero)

    html_bloco = Soup(Sei.driver.page_source, "lxml")
    linhas = html_bloco.find_all(
        "tr", class_=['infraTrClara', 'infraTrEscura'])

    chaves = ['checkbox', 'seq', "processo", 'documento', 'data', 'tipo',
              'assinatura', 'anotacoes', 'acoes']

    lista_processos = []

    for linha in linhas:

        proc = {k: None for k in chaves}

        cols = [v for v in linha.contents if v != "\n"]

        assert len(chaves) == len(cols), "Verifique as linhas do bloco!"

        for k, v in zip(chaves, cols):
            proc[k] = v

        # proc["expedido"] = False

        lista_processos.append(proc)

    return lista_processos


def expedir_bloco(Sei, numero):

    processos = Sei.armazena_bloco(numero)

    for p in processos:

        if pode_expedir(p):
            proc = p['processo'].a.string

            num_doc = p['documento'].a.string

            link = Sei.go(p['processo'].a.attrs['href'])

            (bloco_window, proc_window) = nav_link_to_new_win(
                Sei.driver, link)

            processo = Processo(Sei.driver, proc_window)

            processo.expedir_oficio(proc, num_doc, link)
