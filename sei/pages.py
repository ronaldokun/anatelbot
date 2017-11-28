
# python modules imports
import re

from sei import soup
# INITIALIZE DRIVER
# Exceptions
from sei import TimeoutException

# METHODS
from sei import Keys

# WAIT AND CONDITIONS METHODS
# available since 2.26.0
from sei import Select

# Personal Files
from sei.base import Page

from sei import *


def login_SEI(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    page = Page(driver)
    page.driver.get(loc.Login.URL)
    # page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(loc.Login.LOG)
    senha = page.wait_for_element_to_click(loc.Login.PWD)

    # Clear any clutter on the form
    usuario.clear()
    usuario.send_keys(usr)

    senha.clear()
    senha.send_keys(pwd)

    # Hit Enter
    senha.send_keys(Keys.RETURN)

    return Sei(page.driver)


class Sei(Page):
    """
    Esta subclasse da classe Page define métodos de execução de ações na
    página principal do SEI e de resgate de informações
    """
    def __init__(self, driver):
        super().__init__(driver)
        self._processos = {}

    def processos(self):
        return self._processos.items()
        
    def set_processos(self, processos):
        self._processos = {p['processo'].string : p for p in processos}

    def cria_objeto(self, num, tags):

        return Processo(self.driver, num, tags)


    def ver_proc_detalhado(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.wait_for_element_to_click(loc.Main.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                loc.Main.VISUAL)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def isPaginaInicial(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == loc.Main.TITLE

    def go_to_initial_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        self.wait_for_element_to_click(
            loc.Base.INIT).click()

    def exibir_menu_lateral(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(loc.Base.MENU)

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
        if not self.isPaginaInicial():
            self.go_to_initial_page()

        # Mostra página com informações detalhadas
        self.ver_proc_detalhado()

        contador = Select(self.wait_for_element(loc.Main.CONT))

        pages = [pag.text for pag in contador.options]

        for pag in pages:

            # One simple repetition to avoid more complex code
            contador = Select(self.wait_for_element(loc.Main.CONT))
            contador.select_by_visible_text(pag)
            html_sei = soup(self.driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        # percorre a lista de processos
        # cada linha corresponde a uma tag mãe 'tr'
        # substituimos a tag mãe por uma lista das tags filhas
        # 'tag.contents', descartando os '\n'
        # a função lista_to_dict_tags recebe essa lista e
        # retorna um dicionário das tags
        processos = [ft.armazena_tags(
                         [tag for tag in line.contents if tag != '\n'])
                              for line in processos]

        # processos = {p['processo'].string: p for p in processos}
        
        self.set_processos(processos)
    

class Processo(Sei):

    def __init__(self, driver, numero, tags={}):
        super().__init__(driver)
        self.numero = numero
        self.tags = tags
        self.tree = {}


    def fecha_processo_atual(self):
        self.driver.close()

        
    def info_oficio(self, num_doc):

        assert self.get_title() == Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to tree frame
        self.driver.switch_to_frame("ifrArvore")

        with self.wait_for_page_load():

            html_tree = soup(self.driver.page_source, "lxml")

            info = html_tree.find(title=re.compile(num_doc)).string

            assert info != '', "Falha ao retornar Info do Ofício da Árvore"

            # return to parent frame
            self.driver.switch_to_default_content()

            return info

    def acoes_oficio(self):

        assert self.get_title() == loc.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to central frame
        self.driver.switch_to_frame("ifrVisualizacao")

        self.wait_for_element(loc.Central.ACOES)

        html_frame = soup(self.driver.page_source, "lxml")

        buttons = html_frame.find(id="divArvoreAcoes").contents

        self.driver.switch_to_default_content()

        return buttons

    def atualiza_andamento(self, buttons, info):

        assert self.get_title() == loc.Processo.TITLE, \
            "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = loc.Base.URL + andamento.attrs['href']

        (proc_window, and_window) = ft.nav_link_to_new_win(self.driver, link)

        input_and = self.wait_for_element(ft.Central.IN_AND)

        text = ft.Central.TXT_AND_PRE + info + ft.Central.TXT_AND_POS

        input_and.send_keys(text)

        self.wait_for_element_to_click(ft.Central.SV_AND).click()

        self.driver.close()

        self.driver.switch_to_window(proc_window)

    def enviar_processo_sede(self, buttons):

        with self.wait_for_page_load():

            assert self.get_title() == loc.Processo.TITLE, \
                "Erro na função 'enviar_processo_sede"

            enviar = buttons[3]

            link = loc.Base.URL + enviar.attrs["href"]

            (janela_processo, janela_enviar) = ft.nav_link_to_new_win(
                self.driver, link)

        with self.wait_for_page_load():

            assert self.get_title() == loc.Envio.TITLE, \
                "Erro ao clicar no botão 'Enviar Processo'"

            self.driver.execute_script(loc.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.driver.switch_to_window(janela_unidades)

        assert self.get_title() == loc.Envio.UNIDS, \
            "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.wait_for_element(loc.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(loc.Envio.SIGLA + Keys.RETURN)

        sede = self.wait_for_element(loc.Envio.ID_SEDE)

        assert sede.get_attribute("title") == loc.Envio.SEDE, \
            "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.wait_for_element_to_click(loc.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.driver.close()

        # Troca o foco do navegador
        self.driver.switch_to_window(janela_enviar)

        self.wait_for_element_to_click(loc.Envio.OPEN).click()

        self.wait_for_element_to_click(loc.Envio.RET_DIAS).click()

        prazo = self.wait_for_element(loc.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(loc.Envio.PRAZO)

        self.wait_for_element_to_click(loc.Envio.UTEIS).click()

        self.wait_for_element_to_click(loc.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.driver.close()

        self.driver.switch_to_window(janela_processo)


    def expedir_oficio(self, num_doc):

        info = self.info_oficio(num_doc)

        # self.driver.switch_to_window(self.window)

        buttons = self.acoes_oficio()

        self.atualiza_andamento(buttons, info)

        self.enviar_processo_sede(buttons)

        # self.driver.switch_to_window(main_window)


