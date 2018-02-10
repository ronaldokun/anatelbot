# modules only
import re

import unidecode

from base import Page

from sei import functions as func
from sei import locators

servicos = ('Outorga: Rádio do Cidadão',
            'Outorga: Radioamador',
            'Outorga: Limitado Móvel Aeronáutico',
            'Outorga: Limitado Móvel Marítimo')

def login_sei(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    page = Page(driver)
    page.driver.get(locators.Login.URL)
    # page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(locators.Login.LOG)
    senha = page.wait_for_element_to_click(locators.Login.PWD)

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

    def go(self, link):
        """ Simplifies the navigation of href pages on sei.anatel.gov.br
        by pre-appending the required prefix NAV_URL
       """
        link = locators.Base.URL + link

        self.driver.get(link)

    def get_processos(self):
        return self._processos
        
    def _set_processos(self, processos):
        self._processos = {p['numero']: p for p in processos}

    def _filtra_processos(self, processos, servicos=servicos):
        self._processos = {k: v for k, v in processos.items() if v.get('tipo') in servicos}

    def cria_processo(self, num, tags=None):
        return Processo(self.driver, num, tags)

    def ver_proc_detalhado(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.wait_for_element_to_click(locators.Main.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                locators.Main.VISUAL)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def is_pagina_inicial(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == locators.Main.TITLE

    def go_to_initial_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        self.wait_for_element_to_click(
            locators.Base.INIT).click()

    def exibir_menu_lateral(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(locators.Base.MENU)

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
        if not self.is_pagina_inicial():
            self.go_to_initial_page()

        # Mostra página com informações detalhadas
        self.ver_proc_detalhado()

        contador = Select(self.wait_for_element(locators.Main.CONT))

        paginas = [pag.text for pag in contador.options]

        for pag in paginas:

            # One simple repetition to avoid more complex code
            contador = Select(self.wait_for_element(locators.Main.CONT))
            contador.select_by_visible_text(pag)
            html_sei = Soup(self.driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        processos = [func.armazena_tags(
                    [tag for tag in line.contents if tag != '\n'])
                     for line in processos]

        self._set_processos(processos)

    def contatos_cadastrados(self, nome):

        nome = unidecode._unidecode(nome)

        if self.get_title() != locators.Contato.TITLE:
            self.ir_pagina_contato()

        contato = self.wait_for_element_to_click(locators.Tipos.CONTATO)

        contato.clear()

        contato.send_keys(nome + Keys.RETURN)

        self.wait_for_page_load()


        # if not self.elem_is_visible((By.LINK_TEXT, "Nenhum Registro Encontrado")):

        self.wait_for_element_to_be_visible((By.XPATH, "//*[contains(text(), nome)]"))

        html = Soup(self.driver.page_source, 'lxml')

        tags = html.find_all('tr', class_='infraTrClara')

        return (len(tags), tags) if tags else (0, None)

    def atualiza_elemento(self, id, dado):

        elem = self.wait_for_element(id)

        elem.clear()

        elem.send_keys(dado)

    def atualizar_contato(self, link, dados):

        self.go(link)

        tipo = Select(self.wait_for_element_to_be_visible(locators.Contato.TIPO))

        tipo.select_by_visible_text("Pessoa Física")

        self.wait_for_element_to_click(locators.Contato.PF).click()

        self.atualiza_elemento(locators.Contato.SIGLA, dados['CPF'])

        if dados['SEXO'] == 'MASCULINO':

            self.wait_for_element_to_click(locators.Contato.MASCULINO).click()

        elif dados['SEXO'] == 'FEMININO':

            self.wait_for_element_to_click(locators.Contato.FEMININO).click()

        self.atualiza_elemento(locators.Contato.NOME, dados['NOME'])

        self.atualiza_elemento(locators.Contato.END, dados['ENDERECO'] + ' ' + dados['NUM'])

        self.atualiza_elemento(locators.Contato.COMP, dados['COMP'])

        self.atualiza_elemento(locators.Contato.BAIRRO, dados['BAIRRO'])

        uf = Select(self.wait_for_element(locators.Contato.UF))

        uf.select_by_visible_text(dados['UF'])

        cidade = Select(self.wait_for_element_to_be_visible(locators.Contato.CIDADE))

        cidade.select_by_visible_text(dados["CIDADE"])

        self.atualiza_elemento(locators.Contato.CEP, dados['CEP'])

        self.atualiza_elemento(locators.Contato.CPF, dados['CPF'])

        self.atualiza_elemento(locators.Contato.RG, dados['RG'])

        self.atualiza_elemento(locators.Contato.ORG, dados['ORG'])

        self.atualiza_elemento(locators.Contato.NASC, dados['NASC'])

        self.atualiza_elemento(locators.Contato.FONE, dados['FONE'])

        self.atualiza_elemento(locators.Contato.CEL, dados['CEL'])

        self.atualiza_elemento(locators.Contato.EMAIL, dados['EMAIL'])

        self.wait_for_element_to_click(locators.Contato.SALVAR).click()

    def ir_pagina_contato(self):

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find('li', string='Listar')

        if not tag:
            raise LookupError("The tag of type {0} and string {1} is not present in the page".format('<li>', 'Listar'))

        link = tag.a.attrs['href']

        self.go(link)
    

class Processo(Sei):

    def __init__(self, driver, numero, tags=None):
        super().__init__(driver)
        self.numero = numero
        self.tags = tags
        self.tree = {}

    def fecha_processo_atual(self):
        self.driver.close()

    def info_oficio(self, num_doc):

        assert self.get_title() == locators.Processo.TITLE, \
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

    def acoes_oficio(self):

        assert self.get_title() == locators.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to central frame
        self.driver.switch_to_frame("ifrVisualizacao")

        self.wait_for_element(locators.Central.ACOES)

        html_frame = Soup(self.driver.page_source, "lxml")

        buttons = html_frame.find(id="divArvoreAcoes").contents

        self.driver.switch_to_default_content()

        return buttons

    def atualiza_andamento(self, buttons, info):

        assert self.get_title() == locators.Processo.TITLE, \
            "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = locators.Base.URL + andamento.attrs['href']

        (proc_window, and_window) = func.nav_link_to_new_win(self.driver, link)

        input_and = self.wait_for_element(locators.Central.IN_AND)

        text = locators.Central.AND_PRE + info + locators.Central.AND_POS

        input_and.send_keys(text)

        self.wait_for_element_to_click(locators.Central.SV_AND).click()

        self.driver.close()

        self.driver.switch_to_window(proc_window)

    def enviar_processo_sede(self, buttons):

        with self.wait_for_page_load():

            assert self.get_title() == locators.Processo.TITLE, \
                "Erro na função 'enviar_processo_sede"

            enviar = buttons[3]

            link = locators.Base.URL + enviar.attrs["href"]

            (janela_processo, janela_enviar) = func.nav_link_to_new_win(
                self.driver, link)

        with self.wait_for_page_load():

            assert self.get_title() == locators.Envio.TITLE, \
                "Erro ao clicar no botão 'Enviar Processo'"

            self.driver.execute_script(locators.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.driver.switch_to_window(janela_unidades)

        assert self.get_title() == locators.Envio.UNIDS, \
            "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.wait_for_element(locators.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(locators.Envio.SIGLA + Keys.RETURN)

        sede = self.wait_for_element(locators.Envio.ID_SEDE)

        assert sede.get_attribute("title") == locators.Envio.SEDE, \
            "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.wait_for_element_to_click(locators.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.driver.close()

        # Troca o foco do navegador
        self.driver.switch_to_window(janela_enviar)

        self.wait_for_element_to_click(locators.Envio.OPEN).click()

        self.wait_for_element_to_click(locators.Envio.RET_DIAS).click()

        prazo = self.wait_for_element(locators.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(locators.Envio.PRAZO)

        self.wait_for_element_to_click(locators.Envio.UTEIS).click()

        self.wait_for_element_to_click(locators.Envio.ENVIAR).click()

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

    def limpar_marcadores(self):
        if self.tags.get('anotacao'):
            link = self.tags.get('anotacao_link')

            (main, new) = func.nav_link_to_new_win(self.driver, link)

            postit = self.wait_for_element(Central.IN_POSTIT)

            postit.clear()

            btn = self.wait_for_element_to_click(Central.BT_POSTIT)

            btn.click()

            self.close()

            self.driver.switch_to_window(main)

            self.tags['anotacao'] = ''

        # if self.tags.get('marcador'):
