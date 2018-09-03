# modules only
import re
import os
import sys
import datetime as dt
from contextlib import contextmanager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unidecode
from bs4 import BeautifulSoup as Soup

import functions
from . import sei_helpers
from page import Page
from time import sleep

# Main package
from selenium.common.exceptions import *
# Utilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Methods used from selenium submodules
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import *


SERVICOS = ('Outorga: Rádio do Cidadão',
            'Outorga: Radioamador',
            'Outorga: Limitado Móvel Aeronáutico',
            'Outorga: Limitado Móvel Marítimo')

TRANSLATION = {".": "", "/": "", "-": "", "_": ""}

class make_xlat:

    def __init__(self, *args, **kwds):
        self.adict = dict(*args, **kwds)
        self.rx = self.make_rx( )

    def make_rx(self):
        return re.compile('|'.join(map(re.escape, self.adict)))

    def one_xlat(self, match):
        return self.adict[match.group(0)]

    def __call__(self, text):
        return self.rx.sub(self.one_xlat, text)

strip_processo = make_xlat(TRANSLATION)

def login_sei(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe
    SEI.
    """

    links = sei_helpers.Sei_Base.Login

    page = Page(driver)
    page.driver.get(links.url)
    # page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(links.log)
    senha = page.wait_for_element_to_click(links.pwd)

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

    def __init__(self, driver, processos = None):
        super().__init__(driver)
        self._processos = processos if processos is not None else {}

    def _set_processos(self, processos):

        self._processos = {strip_processo(p['numero']) : p for p in processos}

    def _check_contact(self, nome):

        nome = unidecode._unidecode(nome)

        if self.get_title() != sei_helpers.Contato.TITLE:

            with self.wait_for_page_load():
                self._vai_para_pag_contato()

        try:

            contato = self.wait_for_element_to_click(sei_helpers.Pesq_contato.ID_SEARCH, timeout=5)

        except TimeoutException:

            print("Elemento não encontrado")

            return None

        contato.clear()

        contato.send_keys(nome)

        self.wait_for_element_to_click(sei_helpers.Contato.BTN_PESQUISAR).click()

        sleep(2)

        # if not self.elem_is_visible((By.LINK_TEXT, "Nenhum Registro Encontrado")):

        # self.wait_for_element_to_be_visible((By.PARTIAL_LINK_TEXT, "//*[contains(text(), {}]".format(nome)), timeout=10)

        html = Soup(self.driver.page_source, 'lxml')

        tags = html.find_all('tr', class_='infraTrClara')

        for tag in tags:

            for children in tag.children:

                if hasattr(children, 'text'):

                    if nome.lower() in  str(children.text).lower():

                        return tag.find_all('a')

        else:

            return None

    def _cria_contato(self, dados):

        novo_contato = self.wait_for_element_to_click(sei_helpers.Contato.BTN_NOVO)

        with self.wait_for_page_load():

            novo_contato.click()

        self._mudar_dados_contato(dados, novo=True)

    def _mudar_dados_contato(self, dados, novo=False):

        dados = {k:str(v).title() for k,v in dados.items() if k is not 'UF'}

        dados['UF'] = dados["UF"].upper()

        tipo = self.wait_for_element_to_be_visible(sei_helpers.Contato.TIPO)

        tipo = Select(tipo)

        tipo.select_by_visible_text("Pessoa Física")

        self.wait_for_element_to_click(sei_helpers.Contato.PF).click()

        self._update_elem(sei_helpers.Contato.SIGLA, dados.get('Cpf_RF', ''))

        if dados.get('Sexo', "") == 'FEMININO':

            self.wait_for_element_to_click(sei_helpers.Contato.FEMININO).click()

        else:

            self.wait_for_element_to_click(sei_helpers.Contato.MASCULINO).click()

        self._update_elem(sei_helpers.Contato.NOME, dados.get('Nome', ''))

        self._update_elem(sei_helpers.Contato.END, dados.get('Logradouro', '') + ' ' + dados.get('Num', ''))

        self._update_elem(sei_helpers.Contato.COMP, dados.get('Complemento', ''))

        self._update_elem(sei_helpers.Contato.BAIRRO, dados.get('Bairro', ''))

        pais = self.wait_for_element(sei_helpers.Contato.PAIS)

        pais = Select(pais)

        pais.select_by_visible_text("Brasil")

        uf  = self.wait_for_element(sei_helpers.Contato.UF)

        uf = Select(uf)

        uf.select_by_visible_text(dados.get('UF', ''))

        self._update_elem(sei_helpers.Contato.CEP, dados.get('Cep', ''))

        self._update_elem(sei_helpers.Contato.CPF, dados.get('Cpf_RF', ''))

        self._update_elem(sei_helpers.Contato.RG, dados.get('Rg', ''))

        self._update_elem(sei_helpers.Contato.ORG, dados.get('Org', ''))

        self._update_elem(sei_helpers.Contato.NASC, dados.get('Nasc', ''))

        self._update_elem(sei_helpers.Contato.FONE, dados.get('Fone', ''))

        self._update_elem(sei_helpers.Contato.CEL, dados.get('Cel', ''))

        self._update_elem(sei_helpers.Contato.EMAIL, dados.get('Email', ''))

        # Cidade por último para dar Tempo de Carregamento

        cidade = Select(self.wait_for_element_to_be_visible(sei_helpers.Contato.CIDADE))

        for option in cidade.options:

            ascii_option =  unidecode._unidecode(option.text).lower()

            if dados.get("Cidade", '').lower() == ascii_option:

                cidade. select_by_visible_text(option.text)

                break

        if not novo:

            try:

                salvar = self.wait_for_element_to_click(sei_helpers.Contato.SALVAR)

            except TimeoutException:

                print("Não foi possível salvar o Contato")

                return

        else:


            try:

                salvar = self.wait_for_element_to_click(sei_helpers.Contato.SALVAR_NOVO, timeout=5)

            except TimeoutException:
                print("Não foi possível salvar o Contato")

                return

        with self.wait_for_page_load():

            salvar.click()

    def _vai_para_pag_contato(self):

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find('li', string='Listar')

        if not tag:
            raise LookupError("The tag of type {0} and string {1} is not present in the page".format('<li>', 'Listar'))

        link = tag.a.attrs['href']

        self.go(link)

    def go(self, link):
        """ Simplifies the navigation of href pages on sei.anatel.gov.br
        by pre-appending the required prefix NAV_URL       """

        prefix = sei_helpers.Sei_Base.Base.url

        if prefix not in link:

            link = prefix + link

        self.driver.get(link)

    def get_processos(self):
        return self._processos

    def filter_processos(self, **kwargs):

        processos = {}

        for k,v in kwargs:

            processos = {p : q for p, q in self._processos.items() if p.get(k) == v}

        return processos

    def go_to_processo(self, num):

        striped = strip_processo(num)

        if striped in self._processos.keys():

            self.go(self._processos[striped]['link'])

            return Processo(self.driver, numero=num, tags=self._processos[striped])

        try:

            self._update_elem(sei_helpers.Sei_Base.Base.pesquisa, num + Keys.ENTER)

        except NoSuchElementException:

            self.go_to_init_page()

        return Processo(self.driver, num, tags=None)

    def see_detailed(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.wait_for_element_to_click(sei_helpers.Sei_Inicial.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                sei_helpers.Sei_Inicial.VISUAL)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def is_init_page(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == sei_helpers.Sei_Inicial.TITLE
    # noinspection PyProtectedMember

    def go_to_init_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """

        try:

            self._click_button(sei_helpers.Sei_Base.Base.init)

        except:

            self.go("")

    def show_lat_menu(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(sei_helpers.Sei_Base.menu)

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

        html_sei = Soup(self.driver.page_source, "lxml")

        processos += html_sei("tr", {"class": 'infraTrClara'})


        try:

            contador = self.wait_for_element(sei_helpers.Sei_Inicial.CONT, timeout=30)

        except TimeoutException:

            print("A página demorou muito tempo para carregar ou há somente 1 página de Processos")

            return

        contador = Select(contador)

        paginas = [pag.text for pag in contador.options]

        for pag in paginas:
            # One simple repetition to avoid more complex code
            contador = Select(self.wait_for_element(sei_helpers.Sei_Inicial.CONT))
            contador.select_by_visible_text(pag)
            html_sei = Soup(self.driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        processos_abertos = []

        for line in processos:

            tags = line("td")

            if len(tags) == 6:

                processos_abertos.append(functions.armazena_tags(tags))

        self._set_processos(processos_abertos)

    def atualizar_contato(self, nome, dados):

        tag_contact = self._check_contact(nome)

        if not tag_contact:

            self._cria_contato(dados)

        else:

            for tag in tag_contact:

                for child in tag.children:

                    if hasattr(child, 'attrs'):

                        if child.get('title') == "Alterar Contato":

                            link  = tag.get('href')

                            if link:

                                with self.wait_for_page_load():

                                    self.go(link)

                                self._mudar_dados_contato(dados, novo=False)

                                return

    def pesquisa_contato(self, name):

        if self.get_title() != sei_helpers.Pesq_contato.TITLE:

            self._vai_para_pag_contato()

        pesquisa = self.wait_for_element(sei_helpers.Pesq_contato.ID_SEARCH)

        pesquisa.send_keys(name)

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find_all('td', string=re.compile(".*" + name + ".*"))

        print(tag)

    def cria_processo(self, tipo, desc='', inter='', nivel='público'):

        tipo = str(tipo)

        assert tipo in sei_helpers.Criar_Processo.PROCS, \
            print("O tipo de processo digitado {0}, não é válido".format(str(tipo)))

        self.show_lat_menu()

        init_proc = self.wait_for_element_to_click(sei_helpers.Sei_Menu.INIT_PROC)

        init_proc.click()

        filtro = self.wait_for_element_to_click(sei_helpers.Criar_Processo.FILTRO)

        filtro.send_keys(tipo)

        # exibe_todos = Sei.wait_for_element_to_click(loc.Tipos.EXIBE_ALL)

        # exibe_todos.click()

        # select = Select(Sei.wait_for_element(loc.Tipos.SL_TIP_PROC))

        tipo = self.wait_for_element_to_click((By.LINK_TEXT, tipo))

        tipo.click()

        if desc:
            espec = self.wait_for_element(sei_helpers.Proc_incluir.ESPEC)

            espec.send_keys(desc)

        if inter:

            self.cadastrar_interessado(inter)
            self.consultar_contato(inter)

        if nivel == 'público':

            nivel = self.wait_for_element(sei_helpers.Proc_incluir.PUBL)

        elif nivel == 'restrito':

            nivel = self.wait_for_element(sei_helpers.Proc_incluir.REST)

        else:

            nivel = self.wait_for_element(sei_helpers.Proc_incluir.SIG)

        nivel.click()

class Processo(Sei):

    #TODO: Rastrear Árvore e guardar documentos

    def __init__(self, driver, numero, tags=None):
        super().__init__(driver)
        self.driver = driver
        self.numero = numero
        self.tags = tags if tags is not None else dict()
        self.acoes = {}
        self.arvore = {}
        self.link = self.driver.current_url

    def get_tags(self):
        return self.tags
    @contextmanager
    def _go_to_central_frame(self):

        # Switch to central frame
        self.driver.switch_to.frame("ifrVisualizacao")

        try:
            yield
        finally:
            # Return to main content
            self.driver.switch_to_default_content()

    def _acoes_central_frame(self):

        assert self.get_title() == sei_helpers.Proc_incluir.TITLE, \
            "Erro ao navegar para o processo"

        with self._go_to_central_frame():

            self.wait_for_element(sei_helpers.Proc_central.ACOES)

            html_frame = Soup(self.driver.page_source, "lxml")

            acoes = html_frame.find(id="divArvoreAcoes").contents

            return functions.cria_dict_acoes(acoes)

    def _get_acoes(self, doc=None):

        # O comportamento padrão é extrair as ações do Processo Pai
        if doc is None:

            self._click_na_arvore(self.numero)

        else:

            self._click_na_arvore(doc)

        return self._acoes_central_frame()

    def is_open(self):
        return 'Concluir Processo' in self._get_acoes()

    def close_processo(self):
        self.driver.close()
    @contextmanager
    def _go_to_arvore(self):

        # Switch to tree frame
        self.driver.switch_to.frame("ifrArvore")

        try:
            # yield the iframe page source as a BeautifulSoup object
            yield
        finally:
            # Return to main content
            self.driver.switch_to_default_content()

    def armazena_arvore(self):

        # Switch to the frame in which arvore is in, only inside the contextmanager
        with self._go_to_arvore():

            tree = Soup(self.driver.page_source, "lxml")

            for tag in tree.find_all('a', target=True):

                label = tag.attrs.get('title')

                if label is not None:

                    self.arvore[label.strip()] = tag.attrs

        return self.arvore

    def _click_na_arvore(self, label):

        tree = self.armazena_arvore()

        # self.armazena_arvore updates self.arvore dict and return it
        for k, v in tree.items():

            if label in k:

                with self._go_to_arvore():
                    self._click_button((By.ID, v['id']))

                return

        try:

            with self._go_to_arvore():

                self._click_button((By.LINK_TEXT, self.numero))

                return

        except TimeoutException:

            raise ValueError("Não foi encontrato o elemento {0} na árvore do Processo".format(label))

    def send_doc_por_email(self, label, dados):

        #script = self._get_acoes(num_doc)["Enviar Documento por Correio Eletrônico"]

        helper = sei_helpers.Email

        self._click_na_arvore(label)

        with self._go_to_central_frame():

            #TODO: Why this is not working?
            #self.driver.execute_script(script)

            windows = self.driver.window_handles

            self._click_button((By.XPATH, '//*[@id="divArvoreAcoes"]/a[6]'))

            # This garantes that after we're done the driver will switch to the main content
            with self._go_to_new_win(windows):

                destinatario, assunto, mensagem = dados

                self._update_elem(helper.destinatario, destinatario)

                #ActionChains(self.driver).key_down(Keys.RETURN).perform()

                #self._click_button((By.LINK_TEXT, destinatario))

                self._update_elem(helper.assunto, assunto)

                self._select_by_text(helper.mensagem, mensagem)

                # After putting the email, we must validate ir by clicking it or pressing ENTER
                self._update_elem(helper.destinatario, 2*Keys.ENTER)

                self._click_button(helper.enviar)

    def info_oficio(self, num_doc):

        assert self.get_title() == sei_helpers.Proc_incluir.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to tree frame
        self.go_to_arvore()

        with self.wait_for_page_load():

            html_tree = Soup(self.driver.page_source, "lxml")

            info = html_tree.find(title=re.compile(num_doc)).string

            assert info != '', "Falha ao retornar Info do Ofício da Árvore"

            # return to parent frame
            self.driver.switch_to_default_content()

            return info

    def update_andamento(self, buttons, info):
        assert self.get_title() == sei_helpers.Proc_incluir.TITLE, \
            "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = andamento.attrs['href']

        (proc_window, and_window) = Page.nav_link_to_new_win(self.driver, link)

        input_and = self.wait_for_element(sei_helpers.Proc_central.IN_AND)

        text = sei_helpers.Proc_central.AND_PRE + info + sei_helpers.Proc_central.AND_POS

        input_and.send_keys(text)

        self.wait_for_element_to_click(sei_helpers.Proc_central.SV_AND).click()

        self.driver.close()

        self.driver.switch_to.window(proc_window)

    def send_proc_to_sede(self, buttons):

        with self.wait_for_page_load():
            assert self.get_title() == sei_helpers.Proc_incluir.TITLE, \
                "Erro na função 'send_proc_to_sede"

            enviar = buttons[3]

            link = enviar.attrs["href"]

            (janela_processo, janela_enviar) = Page.nav_link_to_new_win(
                self.driver, link)

        with self.wait_for_page_load():
            assert self.get_title() == sei_helpers.Envio.TITLE, \
                "Erro ao clicar no botão 'Enviar Processo'"

            self.driver.execute_script(sei_helpers.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.driver.switch_to.window(janela_unidades)

        assert self.get_title() == sei_helpers.Envio.UNIDS, \
            "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.wait_for_element(sei_helpers.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(sei_helpers.Envio.SIGLA + Keys.RETURN)

        sede = self.wait_for_element(sei_helpers.Envio.ID_SEDE)

        assert sede.get_attribute("title") == sei_helpers.Envio.SEDE, \
            "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.wait_for_element_to_click(sei_helpers.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.driver.close()

        # Troca o foco do navegador
        self.driver.switch_to.window(janela_enviar)

        self.wait_for_element_to_click(sei_helpers.Envio.OPEN).click()

        self.wait_for_element_to_click(sei_helpers.Envio.RET_DIAS).click()

        prazo = self.wait_for_element(sei_helpers.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(sei_helpers.Envio.PRAZO)

        self.wait_for_element_to_click(sei_helpers.Envio.UTEIS).click()

        self.wait_for_element_to_click(sei_helpers.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.driver.close()

        self.driver.switch_to.window(janela_processo)

    def expedir_oficio(self, num_doc: str):

        info = self.info_oficio(num_doc)

        buttons = self.acoes_processo()

        self.update_andamento(buttons, info)

        self.send_proc_to_sede(buttons)

    def go_to_postit(self):

        link = self._get_acoes().get('Anotações')

        if link is not None:

            main, new = self.nav_link_to_new_win(link)

        else:

            main, new = self.driver.current_window_handle, None

        return main, new

    def edita_postit(self, content='', prioridade=False):

        (main, new) = self.go_to_postit()

        if new is not None:

            postit = self.wait_for_element(sei_helpers.Proc_central.IN_POSTIT)

            postit.clear()

            sleep(1)

            if content != '':
                postit.send_keys(content)

            chk_prioridade = self.wait_for_element_to_click(sei_helpers.Proc_central.CHK_PRIOR)

            if prioridade:

                if not chk_prioridade.is_selected():

                    chk_prioridade.click()

                    sleep(1)

            else:

                if chk_prioridade.is_selected():

                    chk_prioridade.click()

                    sleep(1)

            btn = self.wait_for_element_to_click(sei_helpers.Proc_central.BT_POSTIT)

            btn.click()

            sleep(1)

            self.close()

            self.driver.switch_to.window(main)

            if 'anotacao' and 'anotacao_link' in self.tags:

                self.tags['anotacao'] = content

                self.tags['anotacao_link'] = ''

    def go_to_marcador(self):

        link = self._get_acoes().get("Gerenciar Marcador")

        if link is not None:

            main, new = self.nav_link_to_new_win(link)

            return main, new

        else:

            (None, None)

    def go_to_acomp_especial(self):

        link = self._get_acoes().get("Acompanhamento Especial")

        if link is not None:

            main, new = self.nav_link_to_new_win(link)

            return main, new

        else:

            (self.driver.current_window_handle, None)

    def excluir_acomp_especial(self):

        (main, new) = self.go_to_acomp_especial()

        if new is not None:

            if self.check_element_exists(sei_helpers.Acompanhamento_Especial.EXCLUIR):

                try:

                    self._click_button(sei_helpers.Acompanhamento_Especial.EXCLUIR)

                except TimeoutException:

                    print("Não foi possível excluir o Acompanhamento Especial")

                try:

                    alert = self.alert_is_present(timeout=5)

                except NoAlertPresentException:

                    print("Não houve pop-up de confirmação")

                if alert:

                    alert.accept()

                self.close()

                self.driver.switch_to.window(main)

                self.tags['Acompanhamento Especial'] = ""

    def edita_marcador(self, tipo="", content=''):

        (main, new) = self.go_to_marcador()

        if new is not None:

            self._click_button(sei_helpers.Marcador.SELECT_MARCADOR)

            self._click_button((By.LINK_TEXT, tipo))

            self._update_elem(sei_helpers.Marcador.TXT_MARCADOR, content)

            self._click_button(sei_helpers.Marcador.SALVAR)

            self.close()

            self.driver.switch_to.window(main)

    def _incluir_documento(self, tipo, timeout=5):

        if tipo not in sei_helpers.Gerar_Doc.TIPOS:

            raise ValueError("Tipo de Documento inválido: {}".format(tipo))

        link = self._get_acoes().get('Incluir Documento')

        if link is not None:

            with self.wait_for_page_load():

                self.go(link)

            self._click_button((By.LINK_TEXT, tipo), timeout=timeout)

        else:

            raise ValueError("Problema com o link de ações do processo: 'Incluir Documento'")

    def incluir_oficio(self, tipo, dados=None, anexo=False, acesso='publico', hipotese=None):

        #TODO:Inclui anexo

        helper = sei_helpers.Gerar_Doc.oficio

        if tipo not in sei_helpers.Gerar_Doc.TEXTOS_PADRAO:

            raise ValueError("Tipo de Ofício inválido: {}".format(tipo))

        self._incluir_documento("Ofício")

        self._click_button(helper.get('id_txt_padrao'))

        self._select_by_text(helper.get('id_modelos'), tipo)

        if acesso == 'publico':

            self._click_button(helper.get('id_pub'))

        elif acesso == 'restrito':

            self._click_button(helper.get('id_restrito'))

            hip = Select(self.wait_for_element_to_click(helper.get('id_hip_legal')))

            if hipotese not in helper.HIPOTESES:

                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            hip.select_by_visible_text(hipotese)

        else:

            raise ValueError("Você provavelmente não vai querer mandar um Ofício Sigiloso")

        windows =  self.driver.window_handles

        self._click_button(helper.get('submit'))

        self.wait_for_new_window(windows)

        windows =  self.driver.window_handles

        janela_processo, janela_oficio = windows[-2], windows[-1]

        #self.go_to_processo(self.numero)

        if dados:

            self.driver.switch_to.window(janela_oficio)

            self.editar_oficio(dados)

            #self.close()

        self.driver.switch_to.window(janela_processo)

    def incluir_informe(self):
        pass

    def incluir_doc_externo(self, tipo, path, arvore= '', formato='nato', acesso='publico', hipotese=None, timeout=5):

        helper = sei_helpers.Gerar_Doc.doc_externo

        #if tipo not in helpers.Gerar_Doc.EXTERNO_TIPOS:

        #    raise ValueError("Tipo de Documento Externo Inválido: {}".format(tipo))

        self._incluir_documento("Externo", timeout=timeout)

        self._select_by_text(helper.get('id_tipo'), tipo, timeout=timeout)

        today = dt.datetime.today().strftime("%d%m%Y")

        self._update_elem(helper.get('id_data'), today, timeout=timeout)

        if arvore: self._update_elem(helper.get('id_txt_tree'), arvore, timeout=timeout)

        if formato.lower() == 'nato': self._click_button(helper.get('id_nato'), timeout=timeout)

        if acesso == 'publico':

            self._click_button(helper.get('id_pub'), timeout=timeout)

        elif acesso == 'restrito':

            self._click_button(helper.get('id_restrito'), timeout=timeout)

            if hipotese not in helper.HIPOTESES:

                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            self._select_by_text(helper.get('id_hip_legal'), hipotese, timeout=timeout)

        else:

            raise ValueError("Você provavelmente não vai querer um documento Externo Sigiloso")

        self._update_elem(helper.get('id_file_upload'), path, timeout=timeout)

        self._click_button(helper.get('submit'), timeout=timeout)

        self.go(self.link)

    def editar_oficio(self, dados, existing=False):

        links = sei_helpers.Sei_Base.Oficio

        self.wait_for_element_to_be_visible(links.editor)

        frames = self.driver.find_elements_by_tag_name("iframe")

        while len(frames) < 3:

            sleep(1)

            frames = self.driver.find_elements_by_tag_name("iframe")

        self.driver.switch_to.frame(frames[2]) # text frame

        # TODO: make this more general
        for tag, value in dados.items():

            xpath = r"//p[contains(text(), '{0}')]"

            element = self.wait_for_element((By.XPATH, xpath.format(tag)))

            action = ActionChains(self.driver)

            action.move_to_element_with_offset(element, 5, 5)

            action.click()

            action.perform()

            sleep(1)

            action.key_down(Keys.RETURN)

            action.perform()

            #action.key_down(Keys.DELETE)

            #action.perform()


            script = "arguments[0].innerHTML = `{0}`;".format(value)

            self.driver.execute_script(script, element)

            sleep(0.5)

        self.driver.switch_to.parent_frame()

        self._click_button(links.submit)

        # Necessary steps to save
        #self.driver.execute_script('arguments[0].removeAttribute("aria-disabled")', salvar)

        #self.driver.execute_script('arguments[0].class = "cke_button cke_button__save cke_button_off"', salvar)

        #salvar.click()

        #sleep(5)

        #self.close()

    def concluir_processo(self):

        excluir = self._get_acoes().get('Concluir Processo').strip()

        assert excluir is not None, "A ação 'Concluir Processo não foi armazenada, verfique as ações do Processo"

        # Switch to central frame
        self.driver.switch_to_frame("ifrVisualizacao")

        try:

            self.driver.execute_script(excluir)

        except JavascriptException as e:

            print("One exception was catched: {}".format(repr(e)))

        alert = self.alert_is_present(timeout=5)

        if alert: alert.accept()

        self.driver.switch_to_default_content()

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

            processo.expedir_oficio(num_doc)
