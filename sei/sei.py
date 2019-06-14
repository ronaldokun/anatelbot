# Built-in Libs
import re
import os
import sys
import datetime as dt
from collections import OrderedDict
from time import sleep
from contextlib import contextmanager

# Other Helpful Libs
import unidecode
from bs4 import BeautifulSoup as soup
from typing import Type, Dict, List, Tuple, Sequence

# Selenium Dependencies
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import *
from selenium import webdriver

# Others modules from this package
import functions
from . import sei_helpers
from page import Page


Browser = webdriver


# TODO: Add password Encryption
# TODO: Select Normal/Teste
def login_sei(usr: str, pwd: str, driver: Browser=None, timeout: int=10)-> 'Sei':
    """
    Esta função recebe um objeto Webdrive e as credenciais
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe
    SEI.
    """

    helper = sei_helpers.Sei_Login.Login

    page = Page(driver)
    page.driver.get(helper.get('url'))
    page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(helper.get('log'))
    senha = page.wait_for_element_to_click(helper.get('pwd'))

    # Clear any clutter on the form
    usuario.clear()
    usuario.send_keys(usr)

    senha.clear()
    senha.send_keys(pwd)

    try:
        page._clicar(helper.get('submit'), silent=True, timeout=timeout)

    except TimeoutException:
        # Hit Enter
        senha.send_keys(Keys.RETURN)

    return Sei(page)

class Sei:
    """
    Esta subclasse da classe Page define métodos de execução de ações na
    página principal do SEI e de resgate de informações
    """

    def __init__(self, page: Page, processos=None):
        self.page = page
        self._processos = processos if processos is not None else {}

    def _mudar_lotação(lotação: str)->None:
        pass


    def _set_processos(self, processos):
        self._processos = {p["numero"]: p for p in processos}

    def pesquisa_contato(self, termo: str, timeout: int=10):
        """Pesquisa a existência de cadastro de contato `nome` 
        
        Args:
            termo (str): termo a ser pesquisado
            timeout (int, optional): tempo de espera pelos elementos da página. Defaults to 10.
        """       

        termo = unidecode._unidecode(termo)

        if self.page.get_title() != sei_helpers.Contato.TITLE:
            with self.page.wait_for_page_load():
                self._vai_para_pag_contato()

        try:

            contato = self.page.wait_for_element_to_click(
                sei_helpers.Pesq_contato.ID_SEARCH, timeout=timeout
            )

        except TimeoutException:

            print("Elemento não encontrado")

            return None

        contato.clear()

        contato.send_keys(termo)

        self.page.wait_for_element_to_click(
            sei_helpers.Contato.BTN_PESQUISAR, timeout=timeout
        ).click()

        # sleep(2)

        # if not self.page.elem_is_visible((By.LINK_TEXT, "Nenhum Registro Encontrado")):

        # self.page.wait_for_element_to_be_visible((By.PARTIAL_LINK_TEXT, "//*[contains(text(), {}]".format(nome)), timeout=10)

        html = soup(self.page.driver.page_source, "lxml")

        tags = html.find_all("tr", class_="infraTrClara")

        for tag in tags:

            for children in tag.children:

                if hasattr(children, "text"):

                    if termo.lower() in str(children.text).lower():
                        return tag.find_all("a")

        else:

            return None

    def _cria_contato(self, dados: Dict)-> None:

        novo_contato = self.page.wait_for_element_to_click(sei_helpers.Contato.BTN_NOVO)

        with self.page.wait_for_page_load():
            novo_contato.click()

        self._mudar_dados_contato(dados, novo=True)

    def _mudar_dados_contato(self, dados, novo=False):

        dados = {k: str(v).title() for k, v in dados.items() if k is not "UF"}

        dados["UF"] = dados["UF"].upper()

        tipo = self.page.wait_for_element_to_be_visible(sei_helpers.Contato.TIPO)

        tipo = Select(tipo)

        tipo.select_by_visible_text("Pessoa Física")

        self.page.wait_for_element_to_click(sei_helpers.Contato.PF).click()

        cpf = dados.get("CNPJ/CPF", "")

        cpf = functions.add_point(cpf)

        self.page._atualizar_elemento(sei_helpers.Contato.SIGLA, cpf)

        if dados.get("Sexo", "") == "FEMININO":

            self.page.wait_for_element_to_click(sei_helpers.Contato.FEMININO).click()

        else:

            self.page.wait_for_element_to_click(sei_helpers.Contato.MASCULINO).click()

        self.page._atualizar_elemento(
            sei_helpers.Contato.NOME, dados.get("Nome/Razão Social", "")
        )

        self.page._atualizar_elemento(
            sei_helpers.Contato.END,
            dados.get("Logradouro", "") + " " + dados.get("Número", ""),
        )

        self.page._atualizar_elemento(sei_helpers.Contato.COMP, dados.get("Complemento", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.BAIRRO, dados.get("Bairro", ""))

        pais = self.page.wait_for_element(sei_helpers.Contato.PAIS)

        pais = Select(pais)

        pais.select_by_visible_text("Brasil")

        uf = self.page.wait_for_element(sei_helpers.Contato.UF)

        uf = Select(uf)

        uf.select_by_visible_text(dados.get("UF", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.CEP, dados.get("Cep", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.CPF, dados.get("Cpf_RF", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.RG, dados.get("Rg", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.ORG, dados.get("Org", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.NASC, dados.get("Nasc", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.FONE, dados.get("Fone", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.CEL, dados.get("Cel", ""))

        self.page._atualizar_elemento(sei_helpers.Contato.EMAIL, dados.get("Email", ""))

        # Cidade por último para dar Tempo de Carregamento

        cidade = Select(self.page.wait_for_element_to_be_visible(sei_helpers.Contato.CIDADE))

        for option in cidade.options:

            ascii_option = unidecode._unidecode(option.text).lower()

            if dados.get("Município", "").lower() == ascii_option:
                cidade.select_by_visible_text(option.text)

                break

        if not novo:

            try:

                salvar = self.page.wait_for_element_to_click(sei_helpers.Contato.SALVAR)

            except TimeoutException:

                print("Não foi possível salvar o Contato")

                return

        else:

            try:

                salvar = self.page.wait_for_element_to_click(
                    sei_helpers.Contato.SALVAR_NOVO, timeout=5
                )

            except TimeoutException:
                print("Não foi possível salvar o Contato")

                return

        with self.page.wait_for_page_load():

            salvar.click()

    def _vai_para_pag_contato(self):

        html = soup(self.page.driver.page_source, "lxml")

        tag = html.find("li", string="Listar")

        if not tag:
            raise LookupError(
                "The tag of type {0} and string {1} is not present in the page".format(
                    "<li>", "Listar"
                )
            )

        link = tag.a.attrs["href"]

        self.go(link)

    def go(self, link):
        """ Simplifies the navigation of href pages on sei.anatel.gov.br
        by pre-appending the required prefix NAV_URL       """

        prefix = sei_helpers.Sei_Login.Base.url

        if prefix not in link:
            link = prefix + link

        self.page.driver.get(link)

    def get_processos(self):
        return self._processos

    def filter_processos(self, **kwargs):

        processos = {}

        for k, v in kwargs:
            processos = {p: q for p, q in self._processos.items() if p.get(k) == v}

        return processos

    def go_to_processo(self, num):

        p = self._processos.get(num, None)

        if p is not None:

            self.go(p["link"])

            return Processo(self.page, numero=num, tags=self._processos[num])

        else:

            try:

                self.page._atualizar_elemento(
                    sei_helpers.Sei_Login.Base.pesquisa, num + Keys.ENTER
                )

            except NoSuchElementException:

                self.go_to_init_page()

            return Processo(self.page, num, tags=None)

    def see_detailed(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.page.wait_for_element_to_click(sei_helpers.Sei_Inicial.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print(
                "A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'"
            )

        try:

            visual_detalhado = self.page.wait_for_element_to_click(
                sei_helpers.Sei_Inicial.VISUAL
            )

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print(
                "A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada"
            )

    def is_init_page(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário
        """
        return self.page.get_title() == sei_helpers.Sei_Inicial.TITLE

    # noinspection PyProtectedMember
    def go_to_init_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """

        try:

            self.page._clicar(sei_helpers.Sei_Login.Base.init)

        except:

            self.go("")

    def show_lat_menu(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.page.wait_for_element(sei_helpers.Sei_Login.Base.menu)

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

        html_sei = soup(self.page.driver.page_source, "lxml")

        processos += html_sei("tr", {"class": "infraTrClara"})

        try:

            contador = self.page.wait_for_element(sei_helpers.Sei_Inicial.CONT, timeout=30)

        except TimeoutException:

            print(
                "A página demorou muito tempo para carregar ou há somente 1 página de Processos"
            )

            return

        contador = Select(contador)

        paginas = [pag.text for pag in contador.options]

        counter = 1

        for pag in paginas:
            print("Registrando processos: página {}".format(pag))
            # One simple repetition to avoid more complex code
            contador = Select(self.page.wait_for_element(sei_helpers.Sei_Inicial.CONT))
            contador.select_by_visible_text(pag)

            sleep(10)

            # pattern = re.compile("Lista de Processos\s{1}\((\d+).*\)")

            html_sei = soup(self.page.driver.page_source, "lxml")

            processos += html_sei("tr", {"class": "infraTrClara"})

            counter += 400

        processos_abertos = []

        for line in processos:

            tags = line("td")

            if len(tags) == 6:
                processos_abertos.append(functions.armazena_tags(tags))

        self._set_processos(processos_abertos)

    def atualizar_contato(self, nome, dados):

        tag_contact = self.pesquisa_contato(nome)

        if not tag_contact:

            self._cria_contato(dados)

        else:

            for tag in tag_contact:

                for child in tag.children:

                    if hasattr(child, "attrs"):

                        if child.get("title") == "Alterar Contato":

                            link = tag.get("href")

                            if link:
                                with self.page.wait_for_page_load():
                                    self.go(link)

                                self._mudar_dados_contato(dados, novo=False)

                                return

    def cria_processo(self, tipo, desc="", inter="", nivel="público"):

        tipo = str(tipo)

        assert tipo in sei_helpers.Criar_Processo.PROCS, print(
            "O tipo de processo digitado {0}, não é válido".format(str(tipo))
        )

        self.show_lat_menu()

        init_proc = self.page.wait_for_element_to_click(sei_helpers.Sei_Menu.INIT_PROC)

        init_proc.click()

        filtro = self.page.wait_for_element_to_click(sei_helpers.Criar_Processo.FILTRO)

        filtro.send_keys(tipo)

        # exibe_todos = Sei.wait_for_element_to_click(loc.Tipos.EXIBE_ALL)

        # exibe_todos.click()

        # select = Select(Sei.wait_for_element(loc.Tipos.SL_TIP_PROC))

        tipo = self.page.wait_for_element_to_click((By.LINK_TEXT, tipo))

        tipo.click()

        if desc:
            espec = self.page.wait_for_element(sei_helpers.Proc_incluir.ESPEC)

            espec.send_keys(desc)

        if inter:
            # self.cadastrar_interessado(inter)

            self.pesquisa_contato(inter)

        if nivel == "público":

            nivel = self.page.wait_for_element(sei_helpers.Proc_incluir.PUBL)

        elif nivel == "restrito":

            nivel = self.page.wait_for_element(sei_helpers.Proc_incluir.REST)

        else:

            nivel = self.page.wait_for_element(sei_helpers.Proc_incluir.SIG)

        nivel.click()

class Processo(Sei):
    def __init__(self, page, numero, tags=None):
        super().__init__(page)
        #self.page = page
        self.numero = numero
        self.tags = tags if tags is not None else dict()
        self.acoes = {}
        self.arvore = OrderedDict()
        self.link = self.page.driver.current_url

    def get_tags(self):
        return self.tags

    @contextmanager
    def _go_to_central_frame(self):

        # Switch to central frame
        self.page.driver.switch_to.frame("ifrVisualizacao")

        try:
            yield
        finally:
            # Return to main content
            self.page.driver.switch_to_default_content()

    def _acoes_central_frame(self):

        assert (
            self.page.get_title() == sei_helpers.Proc_incluir.TITLE
        ), "Erro ao navegar para o processo"

        with self._go_to_central_frame():
            self.page.wait_for_element(sei_helpers.Proc_central.ACOES)

            html_frame = soup(self.page.driver.page_source, "lxml")

            acoes = html_frame.find(id="divArvoreAcoes").contents

            return functions.cria_dict_acoes(acoes)

    def _get_acoes(self, doc=None):

        # O comportamento padrão é extrair as ações do Processo Pai
        if doc is None:

            self._click_na_arvore(self.numero)

        else:

            self._click_na_arvore(doc)

        return self._acoes_central_frame()

    def _info_unidades(self):
        #return "Concluir Processo" in self._get_acoes()
        with self._go_to_central_frame():
            source = soup(self.page.driver.page_source, "lxml")
            return source.find("div", id="divInformacao")

    def is_open(self, setor):
        return self._info_unidades().find(string=setor)

    

    def close_processo(self):
        self.page.fechar()

    @contextmanager
    def _go_to_arvore(self):

        # Switch to tree frame
        self.page.driver.switch_to.frame("ifrArvore")

        try:
            # yield the iframe page source as a BeautifulSoup object
            yield
        finally:
            # Return to main content
            self.page.driver.switch_to_default_content()

    def armazena_arvore(self):

        # Switch to the frame in which arvore is in, only inside the contextmanager
        with self._go_to_arvore():

            tree = soup(self.page.driver.page_source, "lxml")

            for tag in tree.find_all("a"):

                child = tag.find("span")

                text = None

                if not child:
                    child = tag.find("img")
                    if child and "title" in child.attrs:
                        text = child["title"]
                elif hasattr(child, "text"):
                    text = child.string
                elif "title" in child.attrs:                
                    text = child["title"]

                if text is not None:
                    self.arvore[text.strip()] = tag.attrs

        return self.arvore

    def _click_na_arvore(self, label, timeout: int = 5):

        tree = self.armazena_arvore()

        # self.armazena_arvore updates self.arvore dict and return it
        for k, v in tree.items():

            if label in k:

                with self._go_to_arvore():
                    self.page._clicar((By.ID, v["id"]), timeout=timeout)

                return

        else:
            raise ValueError(
                "Não foi encontrato o elemento {0} na árvore do Processo".format(label)
            )

        # finally:

    #     with self._go_to_arvore():

    #         self._click_button((By.LINK_TEXT, self.numero), timeout=timeout)

    #         return

    def abrir_pastas(self, timeout: int = 10) -> None:

        h = sei_helpers.Arvore.ABRIR_PASTAS

        tree = self.armazena_arvore()
        
        plus = tree.get("Abrir todas as Pastas")

        if plus:
            with self._go_to_arvore():
                try:
                    self.page._clicar((By.ID, plus["id"]), timeout=timeout)
                except TimeoutException:
                    self.go(plus['href'])

    def edita_doc(self, num_doc, timeout: int = 10)-> None:

        self = Sei.go_to_processo(self, num_doc)

        key = lambda x: x.replace(" ", "_").split("_")[-2]

        with self._go_to_arvore():
            
            doc = self.page.wait_for_element((By.PARTIAL_LINK_TEXT, num_doc), timeout=timeout)

            source = soup(doc.get_attribute("innerHTML"), "lxml")
            
            source = source.find("span") 

            title = source.attrs['title'][:-10] + " - OK" + source.attrs['title'][-10:]

            self.page.driver.execute_script(fr"var elem=arguments[0]; elem.title = '{title}'; elem.text = '{title}'", doc)

            
        #    self.page._clicar(h, timeout=timeout)

    def send_doc_por_email(self, label, dados, timeout=5):

        # script = self._get_acoes(num_doc)["Enviar Documento por Correio Eletrônico"]

        helper = sei_helpers.Email

        self._click_na_arvore(label, timeout=timeout)

        with self._go_to_central_frame():
            # TODO: Why this is not working?
            # self.page.driver.execute_script(script)

            # Usamos um context manager
            # para garantir que depois de finalizar a tarefa na nova janela
            # voltamos o foco do navegador para a janela principal
            with self.page._navega_nova_janela():
                self.page._click_button_new_win((By.XPATH, '//*[@id="divArvoreAcoes"]/a[6]'))

                destinatario, assunto, mensagem = dados

                self.page._atualizar_elemento(
                    helper.get('destinatario'), destinatario, timeout=timeout
                )

                self.page._atualizar_elemento(helper.get('assunto'), assunto, timeout=timeout)

                self.page._selecionar_por_texto(helper.get('mensagem'), mensagem, timeout=timeout)

                # After putting the email, we must validate ir by clicking it or pressing ENTER
                self.page._atualizar_elemento(
                    helper.destinatario, 2 * Keys.ENTER, timeout=timeout
                )

                self.page._clicar(helper.get('enviar'), timeout=timeout)

    def info_oficio(self, num_doc):

        assert (
            self.page.get_title() == sei_helpers.Proc_incluir.TITLE
        ), "Erro ao navegar para o processo"

        # Switch to tree frame
        self._go_to_arvore()

        with self.page.wait_for_page_load():
            html_tree = soup(self.page.driver.page_source, "lxml")

            info = html_tree.find(title=re.compile(num_doc)).string

            assert info != "", "Falha ao retornar Info do Ofício da Árvore"

            # return to parent frame
            self.page.driver.switch_to_default_content()

            return info

    def update_andamento(self, buttons, info):
        assert (
            self.page.get_title() == sei_helpers.Proc_incluir.TITLE
        ), "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = andamento.attrs["href"]

        (proc_window, and_window) = Page.nav_link_to_new_win(self.page.driver, link)

        input_and = self.page.wait_for_element(sei_helpers.Proc_central.IN_AND)

        text = (
            sei_helpers.Proc_central.AND_PRE + info + sei_helpers.Proc_central.AND_POS
        )

        input_and.send_keys(text)

        self.page.wait_for_element_to_click(sei_helpers.Proc_central.SV_AND).click()

        self.page.fechar()

        self.page.driver.switch_to.window(proc_window)

    def send_proc_to_sede(self, buttons):

        with self.page.wait_for_page_load():
            assert (
                self.page.get_title() == sei_helpers.Proc_incluir.TITLE
            ), "Erro na função 'send_proc_to_sede"

            enviar = buttons[3]

            link = enviar.attrs["href"]

            (janela_processo, janela_enviar) = Page.nav_link_to_new_win(
                self.page.driver, link
            )

        with self.page.wait_for_page_load():
            assert (
                self.page.get_title() == sei_helpers.Envio.TITLE
            ), "Erro ao clicar no botão 'Enviar Processo'"

            self.page.driver.execute_script(sei_helpers.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.page.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.page.driver.switch_to.window(janela_unidades)

        assert (
            self.page.get_title() == sei_helpers.Envio.UNIDS
        ), "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.page.wait_for_element(sei_helpers.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(sei_helpers.Envio.SIGLA + Keys.RETURN)

        sede = self.page.wait_for_element(sei_helpers.Envio.ID_SEDE)

        assert (
            sede.get_attribute("title") == sei_helpers.Envio.SEDE
        ), "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.page.wait_for_element_to_click(sei_helpers.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.page.fechar()

        # Troca o foco do navegador
        self.page.driver.switch_to.window(janela_enviar)

        self.page.wait_for_element_to_click(sei_helpers.Envio.OPEN).click()

        self.page.wait_for_element_to_click(sei_helpers.Envio.RET_DIAS).click()

        prazo = self.page.wait_for_element(sei_helpers.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(sei_helpers.Envio.PRAZO)

        self.page.wait_for_element_to_click(sei_helpers.Envio.UTEIS).click()

        self.page.wait_for_element_to_click(sei_helpers.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.page.fechar()

        self.page.driver.switch_to.window(janela_processo)

    def expedir_oficio(self, num_doc: str):

        info = self.info_oficio(num_doc)

        buttons = self._get_acoes()

        self.update_andamento(buttons, info)

        self.send_proc_to_sede(buttons)

    def go_to_postit(self):

        link = self._get_acoes().get("Anotações")

        if link is not None:

            main, new = self.page.nav_link_to_new_win(link)

        else:

            main, new = self.page.driver.current_window_handle, None

        return main, new

    def edita_postit(self, content="", prioridade=False):

        (main, new) = self.go_to_postit()

        if new is not None:

            postit = self.page.wait_for_element(sei_helpers.Proc_central.IN_AND)

            postit.clear()

            sleep(1)

            if content != "":
                postit.send_keys(content)

            chk_prioridade = self.page.wait_for_element_to_click(
                sei_helpers.Proc_central.CHK_PRIOR
            )

            if prioridade:

                if not chk_prioridade.is_selected():
                    chk_prioridade.click()

                    sleep(1)

            else:

                if chk_prioridade.is_selected():
                    chk_prioridade.click()

                    sleep(1)

            btn = self.page.wait_for_element_to_click(sei_helpers.Proc_central.BT_POSTIT)

            btn.click()

            sleep(1)

            selfpage.fechar()

            self.page.driver.switch_to.window(main)

            if "anotacao" and "anotacao_link" in self.tags:
                self.tags["anotacao"] = content

                self.tags["anotacao_link"] = ""

    def go_to_marcador(self):

        link = self._get_acoes().get("Gerenciar Marcador")

        if link is not None:

            self.page.nav_link_to_new_win(link)

        else:

            raise ValueError("Problemas ao retornar o link para o Marcador")

    def go_to_acomp_especial(self):

        link = self._get_acoes().get("Acompanhamento Especial")

        if link is not None:

            main, new = self.page.nav_link_to_new_win(link)

            return main, new

        else:

            return (self.page.driver.current_window_handle, None)

    def excluir_acomp_especial(self):

        (main, new) = self.go_to_acomp_especial()

        if new is not None:

            if self.page.check_element_exists(sei_helpers.Acompanhamento_Especial.EXCLUIR):

                try:

                    self.page._clicar(sei_helpers.Acompanhamento_Especial.EXCLUIR)

                except TimeoutException:

                    print("Não foi possível excluir o Acompanhamento Especial")

                try:

                    alert = self.page.alert_is_present(timeout=5)

                    if alert:
                        alert.accept()

                except NoAlertPresentException:

                    print("Não houve pop-up de confirmação")

                selfpage.fechar()

                self.page.driver.switch_to.window(main)

                self.tags["Acompanhamento Especial"] = ""

    def edita_marcador(self, tipo="", content="", timeout=5):

        with self.page._navega_nova_janela():
            self.go_to_marcador()

            self.page._clicar(sei_helpers.Marcador.SELECT_MARCADOR, timeout=timeout)

            self.page._clicar((By.LINK_TEXT, tipo), timeout=timeout)

            self.page._atualizar_elemento(
                sei_helpers.Marcador.TXT_MARCADOR, content, timeout=timeout
            )

            self.page._clicar(sei_helpers.Marcador.SALVAR, timeout=timeout)

            selfpage.fechar()

        self.page.driver.get(self.link)

    def incluir_interessados(self, dados, checagem=False, timeout=5):

        h = sei_helpers.Selecionar_Contatos

        if not isinstance(dados, list):
            dados = [dados]

        if checagem:
            dados = [self.pesquisa_contato(dado) for dado in dados]
            dados = [d for d in dados if d is not None]

        # with self.page.wait_for_page_load():
        #    Sei.go_to_processo(self, self.numero)

        link = self._get_acoes().get("Consultar/Alterar Processo")

        if link is not None:

            self.go(link)

            with self.page._navega_nova_janela():

                self.page._click_button_new_win(h.LUPA)

                for dado in dados:

                    self.page._atualizar_elemento(
                        h.INPUT_PESQUISAR, dado + Keys.RETURN, timeout=timeout
                    )

                    self.page._clicar(h.BTN_PESQUISAR, timeout=timeout / 2)

                    try:
                        self.page._clicar((By.ID, "chkInfraItem0"), timeout=timeout)

                        self.page._clicar(h.B_TRSP, timeout=timeout / 2)

                    except TimeoutException:
                        next

                # selfpage.fechar()
                self.page._clicar(h.BTN_FECHAR, timeout=timeout / 2)

        self.page._clicar(h.SALVAR, timeout=timeout)

        self.go(self.link)

        self = super().go_to_processo(self.numero)

    def incluir_documento(self, tipo, timeout=5):

        if tipo not in sei_helpers.Gerar_Doc.TIPOS:
            raise ValueError("Tipo de Documento inválido: {}".format(tipo))

        link = self._get_acoes().get("Incluir Documento")

        if link is not None:

            with self.page.wait_for_page_load():

                self.go(link)

            self.page._clicar((By.LINK_TEXT, tipo), timeout=timeout)

        else:

            raise ValueError(
                "Problema com o link de ações do processo: 'Incluir Documento'"
            )

    def incluir_oficio(
        self, tipo, dados=None, anexo=False, acesso="publico", hipotese=None, timeout=5
    ):

        # TODO:Inclui anexo

        helper = sei_helpers.Gerar_Doc.oficio

        if tipo not in sei_helpers.Gerar_Doc.TEXTOS_PADRAO:
            raise ValueError("Tipo de Ofício inválido: {}".format(tipo))

        self.incluir_documento("Ofício", timeout=timeout / 2)

        self.page._clicar(helper.get("id_txt_padrao"), timeout=timeout / 2)

        self.page._selecionar_por_texto(helper.get("id_modelos"), tipo, timeout=timeout / 2)

        # self.page._atualizar_elemento(helper.get('id_dest'), dados["CNPJ/CPF"] + Keys.TAB + Keys.RETURN )

        if acesso == "publico":

            self.page._clicar(helper.get("id_pub"), timeout=timeout / 2)

        elif acesso == "restrito":

            self.page._clicar(helper.get("id_restrito"), timeout=timeout)

            hip = Select(
                self.page.wait_for_element_to_click(
                    helper.get("id_hip_legal"), timeout=timeout
                )
            )

            if hipotese not in sei_helpers.Gerar_Doc.HIPOTESES:
                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            hip.select_by_visible_text(hipotese)

        else:

            raise ValueError(
                "Você provavelmente não vai querer mandar um Ofício Sigiloso"
            )

        with self.page._navega_nova_janela():

            self.page._click_button_new_win(helper.get("submit"), timeout=timeout / 2)

            if dados:

                self.editar_oficio(functions.string_endereço(dados), timeout=timeout)

                selfpage.fechar()

        self.page.driver.get(self.link)

    def incluir_informe(self):
        pass

    def incluir_doc_externo(
        self,
        tipo,
        path,
        arvore="",
        formato="nato",
        acesso="publico",
        hipotese=None,
        timeout=5,
    ):

        helper = sei_helpers.Gerar_Doc.doc_externo

        # if tipo not in helpers.Gerar_Doc.EXTERNO_TIPOS:

        #    raise ValueError("Tipo de Documento Externo Inválido: {}".format(tipo))

        self.incluir_documento("Externo", timeout=timeout)

        self.page._selecionar_por_texto(helper.get("id_tipo"), tipo, timeout=timeout)

        today = dt.datetime.today().strftime("%d%m%Y")

        self.page._atualizar_elemento(helper.get("id_data"), today, timeout=timeout)

        if arvore:
            self.page._atualizar_elemento(helper.get("id_txt_tree"), arvore, timeout=timeout)

        if formato.lower() == "nato":
            self.page._clicar(helper.get("id_nato"), timeout=timeout)

        if acesso == "publico":

            self.page._clicar(helper.get("id_pub"), timeout=timeout)

        elif acesso == "restrito":

            self.page._clicar(helper.get("id_restrito"), timeout=timeout)

            if hipotese not in sei_helpers.Gerar_Doc.HIPOTESES:
                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            self.page._selecionar_por_texto(
                helper.get("id_hip_legal"), hipotese, timeout=timeout
            )

        else:

            raise ValueError(
                "Você provavelmente não vai querer um documento Externo Sigiloso"
            )

        self.page._atualizar_elemento(helper.get("id_file_upload"), path, timeout=timeout)

        self.page._clicar(helper.get("submit"), timeout=2 * timeout)

        self.go(self.link)

    def editar_oficio(self, dados, timeout=5, existing=False):

        links = sei_helpers.Sei_Login.Oficio

        self.page.wait_for_element_to_be_visible(links.editor, timeout=timeout)

        frames = self.page.driver.find_elements_by_tag_name("iframe")

        while len(frames) < 3:

            sleep(1)

            frames = self.page.driver.find_elements_by_tag_name("iframe")

        self.page.driver.switch_to.frame(frames[2])  # text frame

        # TODO: make this more general
        for tag, value in dados.items():
            xpath = r"//p[contains(text(), '{0}')]"

            element = self.page.wait_for_element((By.XPATH, xpath.format(tag)))

            action = ActionChains(self.page.driver)

            action.move_to_element_with_offset(element, 5, 5)

            action.click()

            action.perform()

            sleep(1)

            action.key_down(Keys.RETURN)

            action.perform()

            # action.key_down(Keys.DELETE)

            # action.perform()

            script = "arguments[0].innerHTML = `{0}`;".format(value)

            self.page.driver.execute_script(script, element)

            sleep(2)

        self.page.driver.switch_to.parent_frame()

        self.page._clicar(links.submit, timeout=timeout)

        # Necessary steps to save
        # self.page.driver.execute_script('arguments[0].removeAttribute("aria-disabled")', salvar)

        # self.page.driver.execute_script('arguments[0].class = "cke_button cke_button__save cke_button_off"', salvar)

        # salvar.click()

        # sleep(5)

        # selfpage.fechar()

    def concluir_processo(self):

        excluir = self._get_acoes().get("Concluir Processo").strip()

        assert (
            excluir is not None
        ), "A ação 'Concluir Processo não foi armazenada, verfique as ações do Processo"

        # Switch to central frame
        self.page.driver.switch_to_frame("ifrVisualizacao")

        try:

            self.page.driver.execute_script(excluir)

        except JavascriptException as e:

            print("One exception was catched: {}".format(repr(e)))

        alert = self.page.alert_is_present(timeout=5)

        if alert:
            alert.accept()

        self.page.driver.switch_to_default_content()


def exibir_bloco(sei, numero):
    if sei.get_title() != sei_helpers.Blocos.TITLE:
        sei.go_to_blocos()

    try:
        sei.wait_for_element((By.LINK_TEXT, str(numero))).click()

    except:
        print(
            "O Bloco de Assinatura informado não existe ou está \
              concluído!"
        )


def armazena_bloco(sei, numero):
    if sei.get_title() != sei_helpers.Bloco.TITLE + " " + str(numero):
        sei.exibir_bloco(numero)

    html_bloco = soup(sei.driver.page_source, "lxml")
    linhas = html_bloco.find_all("tr", class_=["infraTrClara", "infraTrEscura"])

    chaves = [
        "checkbox",
        "seq",
        "processo",
        "documento",
        "data",
        "tipo",
        "assinatura",
        "anotacoes",
        "acoes",
    ]

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


def expedir_bloco(sei, numero):
    processos = sei.armazena_bloco(numero)

    for p in processos:

        if functions.pode_expedir(p):
            proc = p["processo"].a.string

            num_doc = p["documento"].a.string

            link = sei.go(p["processo"].a.attrs["href"])

            (bloco_window, proc_window) = Page.nav_link_to_new_win(sei.driver, link)

            processo = Processo(sei.driver, proc_window)

            processo.expedir_oficio(num_doc)
