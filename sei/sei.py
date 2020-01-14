# Built-in Libs
import datetime as dt
import re
from collections import OrderedDict
from contextlib import contextmanager
from time import sleep
from typing import Any, Dict, Union

# Other Helpful Libs
# import unidecode
from bs4 import BeautifulSoup as soup

# Selenium Dependencies
from selenium.common.exceptions import (
    JavascriptException,
    NoAlertPresentException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Others modules from this package
from tools.functions import add_point_cpf_cnpj, get_browser
from tools.page import Page

from . import config, context
from .common import armazena_tags, cria_dict_acoes, pode_expedir, string_endereço

Processos = Dict[str, Any]


# TODO: Add password Encryption
# TODO: Select Normal/Teste
# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember
def login_sei(
    usr: str,
    pwd: str,
    browser: str = None,
    timeout: int = 10,
    teste: bool = False,
    is_headless: bool = False,
) -> Union["Sei", None]:
    """
    Esta função recebe uma string com o nome do webdriver, e as credenciais
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe
    SEI.
    """

    helper = config.Sei_Login.Login
    if browser is None:
        browser = "Firefox"
    driver = get_browser(browser=browser, is_headless=is_headless)

    page = Page(driver)
    page.timeout = timeout
    url = "url_teste" if teste else "url"
    try:
        page.driver.get(helper.get(url))
    except WebDriverException as e:
        print("Problema ao carregar a página")
        repr(e)
        return None
    page.driver.maximize_window()

    page._atualizar_elemento(helper.get("log"), usr)
    page._atualizar_elemento(helper.get("pwd"), pwd)

    page._clicar(helper.get("submit"), silent=True)

    return Sei(page, teste=teste)


class Sei:
    """Esta subclasse da classe Page define métodos de execução de ações na
    página principal do SEI e de resgate de informações
    """

    def __init__(
        self, page: Page, processos: Processos = None, teste: bool = False
    ) -> None:
        self.teste = teste
        self.page = page
        self._processos = processos if processos is not None else OrderedDict()

    # noinspection PyProtectedMember
    def mudar_lotação(self, lotação: str) -> None:

        h = config.SeiHeader

        self.page._selecionar_por_texto(h.LOTACAO, lotação)

    def _set_processos(self, processos) -> None:
        self._processos = OrderedDict((p["numero"], p) for p in processos)

    # TODO: generalize
    # DEPRECATED
    def pesquisa_contato(self, termo: str):
        """Pesquisa a existência de cadastro de contato `nome`

        Args:
            termo (str): termo a ser pesquisado
        """
        helper = config.Contato

        # termo = unidecode._unidecode(termo)

        if self.page.get_title() != helper.TITLE:
            with self.page.wait_for_page_load():
                self._vai_para_pag_contato()

        self.page._atualizar_elemento(config.Pesq_contato.ID_SEARCH, termo)
        self.page._clicar(helper.BTN_PESQUISAR)

        html = soup(self.page.driver.page_source, "lxml")

        tags = html.find_all("tr", class_="infraTrClara")
        print(tags)
        for tag in tags:
            print(tag.children)
            for children in tag.children:

                if hasattr(children, "text"):
                    attr = children.text
                elif hasattr(children, "title"):
                    attr = children.title
                if termo.lower() in str(attr).lower():
                    return tag.find_all("a")

        else:

            return None

    # noinspection PyProtectedMember
    def _cria_contato(self, dados: Dict) -> None:
        helper = config.Contato

        with self.page.wait_for_page_load():
            self.page._clicar(helper.BTN_NOVO)

            self._mudar_dados_contato(dados, novo=True)

    # DEPRECATED
    def _mudar_dados_contato(self, dados: Dict, novo=False):
        helper = config.Contato

        dados = {k: str(v).title() for k, v in dados.items() if k is not "UF"}

        dados["UF"] = dados["UF"].upper()

        self.page._selecionar_por_texto(helper.TIPO, "Pessoa Física")

        self.page._clicar(helper.PF)

        cpf = dados.get("CNPJ/CPF", "")

        cpf = add_point_cpf_cnpj(cpf)

        self.page._atualizar_elemento(helper.SIGLA, cpf)

        if dados.get("Sexo", "") == "FEMININO":
            self.page._clicar(helper.FEMININO)
        else:
            self.page._clicar(helper.MASCULINO)

        # TODO: Criar função auxiliar page.atualizar_elementos

        self.page._atualizar_elemento(helper.NOME, dados.get("Nome/Razão Social", ""))

        self.page._atualizar_elemento(
            helper.END, dados.get("Logradouro", "") + " " + dados.get("Número", "")
        )

        self.page._atualizar_elemento(helper.COMP, dados.get("Complemento", ""))

        self.page._atualizar_elemento(helper.BAIRRO, dados.get("Bairro", ""))

        self.page._selecionar_por_texto(helper.PAIS, "Brasil")

        self.page._selecionar_por_texto(helper.UF, dados.get("UF", ""))

        self.page._atualizar_elemento(helper.CEP, dados.get("Cep", ""))

        self.page._atualizar_elemento(helper.CPF, dados.get("Cpf_RF", ""))

        self.page._atualizar_elemento(helper.RG, dados.get("Rg", ""))

        self.page._atualizar_elemento(helper.ORG, dados.get("Org", ""))

        self.page._atualizar_elemento(helper.NASC, dados.get("Nasc", ""))

        self.page._atualizar_elemento(helper.FONE, dados.get("Fone", ""))

        self.page._atualizar_elemento(helper.CEL, dados.get("Cel", ""))

        self.page._atualizar_elemento(helper.EMAIL, dados.get("Email", ""))

        # Cidade por último para dar Tempo de Carregamento
        cidade = Select(self.page.wait_for_element_to_be_visible(helper.CIDADE))

        for option in cidade.options:

            ascii_option = unidecode._unidecode(option.text).lower()

            if dados.get("Município", "").lower() == ascii_option:
                cidade.select_by_visible_text(option.text)
                break

        if not novo:
            self.page._clicar(helper.SALVAR)
        else:
            self.page._clicar(helper.SALVAR_NOVO)

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

        base = config.Sei_Login.Base

        prefix = base["url_teste"] if self.teste else base["url"]

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

    # noinspection PyProtectedMember
    def go_to_processo(self, num: str) -> "Processo":
        p = self._processos.get(num, None)

        if p is not None:

            self.go(p["link"])

            return Processo(self.page, numero=num, tags=self._processos[num])

        else:

            try:

                self.page._atualizar_elemento(
                    config.Sei_Login.Base["pesquisa"], num + Keys.ENTER
                )

            except NoSuchElementException:

                self.go_to_init_page()

            return Processo(self.page, num, tags=None)

    def ver_todos(self):
        """Expanda a visualização na página inicial para todos os processos.
        """
        self.go_to_init_page()

        html = soup(self.page.driver.page_source, "lxml")

        tag = html.find("a", string=config.Sei_Inicial.VER_TODOS[1])

        if not tag:
            return  # Já está na visualização geral

        try:
            self.page._clicar(config.Sei_Inicial.VER_TODOS)
        except (NoSuchElementException, TimeoutException):
            print(
                "Não foi possível exibir todos os processos ou já se encontram exibidos."
            )

    def ver_detalhado(self):
        """
        Expands the visualization from the main page in SEI
        """
        self.go_to_init_page()

        html = soup(self.page.driver.page_source, "lxml")

        tag = html.find("a", string=config.Sei_Inicial.VER_DET[1])

        if not tag:
            return  # Já está na visualização geral

        try:
            self.page._clicar(config.Sei_Inicial.VER_DET)
        except (NoSuchElementException, TimeoutException):
            print(
                "Não foi possível exibir a visualização detalhada ou a página já se encontra exibida."
            )

    def is_init_page(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário
        """
        return self.page.get_title() == config.Sei_Inicial.TITLE

    # noinspection PyProtectedMember
    def go_to_init_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        if self.is_init_page():
            return
        try:

            self.page._clicar(config.Sei_Login.Base["init"])

        except NoSuchElementException:

            self.go("")

    def show_lat_menu(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.page.wait_for_element(config.Sei_Login.Base["menu"])

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()

    # noinspection PyProtectedMember,PyProtectedMember
    def itera_processos(self):
        """
        Navega as páginas de processos abertos no SEI e guarda as tags
        html dos processos como objeto soup no atributo processos_abertos
        """
        h = config.Sei_Inicial

        # Apaga o conteúdo atual da lista de processos
        processos = []

        self.go_to_init_page()
        self.ver_todos()
        self.ver_detalhado()

        self.page._clicar_se_existir(h.BOT_PAG_1)

        html_sei = soup(self.page.driver.page_source, "lxml")

        processos += html_sei("tr", {"class": "infraTrClara"})

        while self.page._clicar_se_existir(h.NEXT_PAG):

            html_sei = soup(self.page.driver.page_source, "lxml")

            processos += html_sei("tr", {"class": "infraTrClara"})

        processos_abertos = []

        for line in processos:

            tags = line("td")

            if len(tags) == 6:
                processos_abertos.append(armazena_tags(tags))

        self._set_processos(processos_abertos)

    # DEPRECATED
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

    def go_to_blocos(self):

        html = soup(self.page.driver.page_source, "lxml")

        tag = html.find("li", string="Blocos de Assinatura")

        if not tag:
            raise NoSuchElementException(
                "Não foi possível navegar para os Blocos de Assinatura"
            )

        link = tag.a.attrs["href"]

        self.go(link)

    def exibir_bloco(self, numero):
        if self.page.get_title() != config.Blocos.TITLE:
            self.go_to_blocos()
        if not self.page._clicar_se_existir(("link text", str(numero))):
            print(f"O Bloco de Assinatura {numero} não existe ou está concluído!")

    def criar_processo(
        self,
        tipo,
        especificacao="",
        interessado="",
        obs="",
        nivel="público",
        salvar: bool = False,
    ):
        tipo = str(tipo)

        assert tipo in config.Iniciar_Processo.PROCS, print(
            "O tipo de processo digitado {0}, não é válido".format(str(tipo))
        )

        helper = config.Iniciar_Processo

        self.show_lat_menu()

        self.page._clicar(config.Sei_Menu.INIT_PROC)

        self.page._clicar(config.Iniciar_Processo.EXIBE_ALL)

        self.page._clicar((By.LINK_TEXT, tipo))

        if especificacao:
            self.page._atualizar_elemento(helper.ESPEC, especificacao)

        if interessado:

            with self.page._go_new_win():
                self.page._clicar(helper.LUPA["el"])

                campo = config.Selecionar_Contatos.INPUT_PESQUISAR

                self.page._atualizar_elemento(campo, interessado)


        if obs:
            self.page._atualizar_elemento(helper.OBS, obs)

        if nivel == "público":
            self.page._clicar(helper.PUBL)

        elif nivel == "restrito":
            self.page._clicar(helper.REST)

        else:
            self.page._clicar(helper.SIG)

        if salvar:

            try:
                self.page._clicar(helper.SALVAR["el"])
            except (TimeoutException, NoSuchElementException):
                self.page.driver.execute_script(helper.SALVAR["js"])


class Processo(Sei):
    def __init__(self, page, numero, tags=None):
        super().__init__(page)
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
            self.page.get_title() == config.Iniciar_Processo.TITLE
        ), "Erro ao navegar para o processo"

        with self._go_to_central_frame():
            try:
                self.page.wait_for_element(config.Proc_central.ACOES)
            except TimeoutException:
                print("Não foi possível acessar o frame central")
                return {}

            html_frame = soup(self.page.driver.page_source, "lxml")

            acoes = html_frame.find(id="divArvoreAcoes").contents

            return cria_dict_acoes(acoes)

    def _get_acoes(self, doc=None, click=True):

        # O comportamento padrão é extrair as ações do Processo Pai
        if click:
            if doc is None:
                self._click_na_arvore(self.numero)
            else:
                self._click_na_arvore(doc)

        return self._acoes_central_frame()

    # TODO: Retornar lista de setores e atribuições
    def _info_unidades(self) -> str:
        # self._get_acoes()
        with self._go_to_central_frame():
            source = soup(self.page.driver.page_source, "lxml")
            result = source.find("div", id="divInformacao")
            if hasattr(result, "text"):
                return result.text
            else:
                ""

    def is_open(self, setor: str = None):
        info_unidades = self._info_unidades()
        if setor is not None:
            return setor in info_unidades
        return info_unidades

    def close_processo(self):
        self.page.fechar()

    def concluir_processo(self):

        assert (
            self.page.get_title() == config.Iniciar_Processo.TITLE
        ), "Erro ao navegar para o processo"

        concluir = self._get_acoes(click=False).get("Concluir Processo")

        if concluir is not None:
            with self._go_to_central_frame():
                self.page._clicar(concluir)

    def abrir_processo(self):

        assert (
            self.page.get_title() == config.Iniciar_Processo.TITLE
        ), "Erro ao navegar para o processo"

        abrir = self._get_acoes(click=False).get("Reabrir Processo")

        if abrir is not None:
            with self._go_to_central_frame():
                self.page._clicar(abrir)

    # todo: Implementar click_central_frame

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

    # noinspection PyProtectedMember
    def _click_na_arvore(self, label):

        if not self.arvore:
            self.armazena_arvore()
        tree = self.arvore

        # self.armazena_arvore updates self.arvore dict and return it
        for k, v in tree.items():

            if label in k:
                with self._go_to_arvore():
                    self.page._clicar((By.ID, v["id"]))
                return

        else:
            raise ValueError(
                "Não foi encontrato o elemento {0} na árvore do Processo".format(label)
            )

    # TODO: Eliminate Visual Dependency
    def abrir_pastas(self) -> None:

        h = config.Arvore

        with self._go_to_arvore():
            if self.page.check_element_exists(h.ABRIR_PASTAS):
                self.page._clicar(h.ABRIR_PASTAS)

    def send_doc_por_email(self, label, dados):

        # script = self._get_acoes(num_doc)["Enviar Documento por Correio Eletrônico"]
        helper = config.Enviar_Doc_Email

        # self._click_na_arvore(label, timeout=self.timeout)

        env_email = self._get_acoes(label).get(
            "Enviar Documento por Correio Eletrônico"
        )

        destinatario, assunto, mensagem, txt_mensagem = dados

        if env_email:
            with self._go_to_central_frame():
                with self.page._clica_abre_nova_janela(env_email):

                    self.page._atualizar_elemento(helper.get("destinatario"), destinatario)

                    self.page._atualizar_elemento(helper.get("assunto"), assunto)

                    if mensagem:
                        self.page._selecionar_por_texto(helper.get('mensagem'), mensagem)

                    if txt_mensagem:

                        self.page._atualizar_elemento(helper.get('txt_mensagem'), txt_mensagem)

                    # After putting the email, we must validate it by clicking it or pressing ENTER
                    self.page._atualizar_elemento(helper["destinatario"], 2 * Keys.ENTER)

                    self.page._clicar(helper.get("enviar"))

    def info_oficio(self, num_doc):

        assert (
            self.page.get_title() == config.Iniciar_Processo.TITLE
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

    # TODO: Mudar verificação para bs4
    # TODO: Criar helper para verificação bs4 DRY principle
    def update_andamento(self, buttons, info):
        assert (
            self.page.get_title() == config.Iniciar_Processo.TITLE
        ), "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = andamento.attrs["href"]

        (proc_window, and_window) = Page.nav_link_to_new_win(self.page.driver, link)

        input_and = self.page.wait_for_element(config.Proc_central.IN_AND)

        text = config.Proc_central.AND_PRE + info + config.Proc_central.AND_POS

        input_and.send_keys(text)

        self.page.wait_for_element_to_click(config.Proc_central.SV_AND).click()

        self.page.fechar()

        self.page.driver.switch_to.window(proc_window)

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def send_proc_to_sede(self, buttons):

        with self.page.wait_for_page_load():
            assert (
                self.page.get_title() == config.Iniciar_Processo.TITLE
            ), "Erro na função 'send_proc_to_sede"

            enviar = buttons[3]

            link = enviar.attrs["href"]

            (janela_processo, janela_enviar) = Page.nav_link_to_new_win(
                self.page.driver, link
            )

        with self.page.wait_for_page_load():
            assert (
                self.page.get_title() == config.Envio.TITLE
            ), "Erro ao clicar no botão 'Enviar Processo'"

            self.page.driver.execute_script(config.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.page.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.page.driver.switch_to.window(janela_unidades)

        assert (
            self.page.get_title() == config.Envio.UNIDS
        ), "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.page.wait_for_element(config.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(config.Envio.SIGLA + Keys.RETURN)

        sede = self.page.wait_for_element(config.Envio.ID_SEDE)

        assert (
            sede.get_attribute("title") == config.Envio.SEDE
        ), "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.page.wait_for_element_to_click(config.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.page.fechar()

        # Troca o foco do navegador
        self.page.driver.switch_to.window(janela_enviar)

        self.page.wait_for_element_to_click(config.Envio.OPEN).click()

        self.page.wait_for_element_to_click(config.Envio.RET_DIAS).click()

        prazo = self.page.wait_for_element(config.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(config.Envio.PRAZO)

        self.page.wait_for_element_to_click(config.Envio.UTEIS).click()

        self.page.wait_for_element_to_click(config.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.page.fechar()

        self.page.driver.switch_to.window(janela_processo)

    def expedir_oficio(self, num_doc: str):

        info = self.info_oficio(num_doc)

        buttons = self._get_acoes()

        self.update_andamento(buttons, info)

        self.send_proc_to_sede(buttons)

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def go_to_postit(self):

        link = self._get_acoes().get("Anotações")

        if link is not None:

            main, new = self.page.nav_link_to_new_win(link)

        else:

            main, new = self.page.driver.current_window_handle, None

        return main, new

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def edita_postit(self, content="", prioridade=False):

        (main, new) = self.go_to_postit()

        if new is not None:

            postit = self.page.wait_for_element(config.Proc_central.IN_AND)

            postit.clear()

            sleep(1)

            if content != "":
                postit.send_keys(content)

            chk_prioridade = self.page.wait_for_element_to_click(
                config.Proc_central.CHK_PRIOR
            )

            if prioridade:

                if not chk_prioridade.is_selected():
                    chk_prioridade.click()

                    sleep(1)

            else:

                if chk_prioridade.is_selected():
                    chk_prioridade.click()

                    sleep(1)

            btn = self.page.wait_for_element_to_click(config.Proc_central.BT_POSTIT)

            btn.click()

            sleep(1)

            self.page.fechar()

            self.page.driver.switch_to.window(main)

            if "anotacao" and "anotacao_link" in self.tags:
                self.tags["anotacao"] = content

                self.tags["anotacao_link"] = ""

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def go_to_marcador(self):

        link = self._get_acoes().get("Gerenciar Marcador")

        if link is not None:

            self.page.nav_link_to_new_win(link)

        else:

            raise ValueError("Problemas ao retornar o link para o Marcador")

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def go_to_acomp_especial(self):

        link = self._get_acoes().get("Acompanhamento Especial")

        if link is not None:

            main, new = self.page.nav_link_to_new_win(link)

            return main, new

        else:

            return (self.page.driver.current_window_handle, None)

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def excluir_acomp_especial(self):

        (main, new) = self.go_to_acomp_especial()

        if new is not None:

            if self.page.check_element_exists(config.Acompanhamento_Especial.EXCLUIR):

                try:

                    self.page._clicar(config.Acompanhamento_Especial.EXCLUIR)

                except TimeoutException:

                    print("Não foi possível excluir o Acompanhamento Especial")

                try:

                    alert = self.page.alert_is_present()

                    if alert:
                        alert.accept()

                except NoAlertPresentException:

                    print("Não houve pop-up de confirmação")

                self.page.fechar()

                self.page.driver.switch_to.window(main)

                self.tags["Acompanhamento Especial"] = ""

    def edita_marcador(self, tipo="", content="", timeout=5):

        with self.page._go_new_win():
            self.go_to_marcador()

            self.page._clicar(config.Marcador.SELECT_MARCADOR)

            self.page._clicar((By.LINK_TEXT, tipo))

            self.page._atualizar_elemento(config.Marcador.TXT_MARCADOR, content)

            self.page._clicar(config.Marcador.SALVAR)

            self.page.fechar()

        self.page.driver.get(self.link)

    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def incluir_interessados(self, dados, checagem=False, timeout=5):

        h = config.Selecionar_Contatos

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

            with self.page._go_new_win():

                self.page._clica_abre_nova_janela(h.LUPA)

                for dado in dados:

                    self.page._atualizar_elemento(h.INPUT_PESQUISAR, dado + Keys.RETURN)

                    self.page._clicar(h.BTN_PESQUISAR)

                    try:
                        self.page._clicar((By.ID, "chkInfraItem0"))

                        self.page._clicar(h.B_TRSP)

                    except TimeoutException:
                        next

                # selfpage.fechar()
                self.page._clicar(h.BTN_FECHAR)

        self.page._clicar(h.SALVAR)

        self.go(self.link)

        self = super().go_to_processo(self.numero)

    # noinspection PyProtectedMember
    # TODO: Update to bs4 and to use page methods
    # TODO: Replicate logic of send_doc_por_email
    def incluir_documento(self, tipo):

        if tipo not in config.Gerar_Doc.TIPOS:
            raise ValueError("Tipo de Documento inválido: {}".format(tipo))

        doc_incluir = self._get_acoes().get("Incluir Documento")

        if doc_incluir is not None:

            with self._go_to_central_frame():
                self.page._clicar(doc_incluir)
                self.page._clicar((By.LINK_TEXT, tipo))

        else:

            raise ValueError(
                "Problema com o link de ações do processo: 'Incluir Documento'"
            )

    def incluir_doc_sei(
        self, tipo: str, txt_inicial: str, acesso="publico", hipotese=None
    ):

        # txt = unidecode.unidecode(txt_inicial).lower()

        txt = txt_inicial.lower()

        assert txt in ("modelo", "padrao", "nenhum"), f"Opção Inválida: {txt_inicial}"

        helper = config.Gerar_Doc.oficio

        if tipo not in config.Gerar_Doc.TEXTOS_PADRAO:
            raise ValueError("Tipo de Ofício inválido: {}".format(tipo))

        self.incluir_documento("Ofício")

        self.page._clicar(helper.get("id_txt_padrao"))

        self.page._selecionar_por_texto(helper.get("id_modelos"), tipo)

        if acesso == "publico":

            self.page._clicar(helper.get("id_pub"))

        elif acesso == "restrito":

            self.page._clicar(helper.get("id_restrito"))

            hip = Select(
                self.page.wait_for_element_to_click(helper.get("id_hip_legal"))
            )

            if hipotese not in config.Gerar_Doc.HIPOTESES:
                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            hip.select_by_visible_text(hipotese)

        else:

            raise ValueError(
                "Você provavelmente não vai querer mandar um Ofício Sigiloso"
            )

        with self.page._go_new_win():

            self.page._clica_abre_nova_janela(helper.get("submit"))

            if dados:
                self.editar_oficio(string_endereço(dados), timeout=10)

                self.page.fechar()

        self.page.driver.get(self.link)

    def incluir_oficio(
        self, tipo, dados=None, anexo=False, acesso="publico", hipotese=None
    ):

        # TODO:Inclui anexo

        helper = config.Gerar_Doc.oficio

        if tipo not in config.Gerar_Doc.TEXTOS_PADRAO:
            raise ValueError("Tipo de Ofício inválido: {}".format(tipo))

        self.incluir_documento("Ofício")

        self.page._clicar(helper.get("id_txt_padrao"))

        self.page._selecionar_por_texto(helper.get("id_modelos"), tipo)

        if acesso == "publico":

            self.page._clicar(helper.get("id_pub"))

        elif acesso == "restrito":

            self.page._clicar(helper.get("id_restrito"))

            hip = Select(
                self.page.wait_for_element_to_click(helper.get("id_hip_legal"))
            )

            if hipotese not in config.Gerar_Doc.HIPOTESES:
                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            hip.select_by_visible_text(hipotese)

        else:

            raise ValueError(
                "Você provavelmente não vai querer mandar um Ofício Sigiloso"
            )

        with self.page._go_new_win():

            self.page._clica_abre_nova_janela(helper.get("submit"))

            if dados:
                self.editar_oficio(string_endereço(dados), timeout=10)

                self.page.fechar()

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

        helper = config.Gerar_Doc.doc_externo

        # if tipo not in helpers.Gerar_Doc.EXTERNO_TIPOS:

        #    raise ValueError("Tipo de Documento Externo Inválido: {}".format(tipo))

        self.incluir_documento("Externo", timeout=10)

        self.page._selecionar_por_texto(helper.get("id_tipo"), tipo)

        today = dt.datetime.today().strftime("%d%m%Y")

        self.page._atualizar_elemento(helper.get("id_data"), today)

        if arvore:
            self.page._atualizar_elemento(helper.get("id_txt_tree"), arvore)

        if formato.lower() == "nato":
            self.page._clicar(helper.get("id_nato"))

        if acesso == "publico":

            self.page._clicar(helper.get("id_pub"))

        elif acesso == "restrito":

            self.page._clicar(helper.get("id_restrito"))

            if hipotese not in config.Gerar_Doc.HIPOTESES:
                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            self.page._selecionar_por_texto(helper.get("id_hip_legal"), hipotese)

        else:

            raise ValueError(
                "Você provavelmente não vai querer um documento Externo Sigiloso"
            )

        self.page._atualizar_elemento(helper.get("id_file_upload"), path)

        self.page._clicar(helper.get("submit"))

        self.go(self.link)

    # noinspection PyProtectedMember
    def editar_oficio(self, dados, timeout=5, existing=False):

        links = config.Sei_Login.Oficio

        self.page.wait_for_element_to_be_visible(links.editor)

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

        self.page._clicar(links.submit)

        # Necessary steps to save
        # self.page.driver.execute_script('arguments[0].removeAttribute("aria-disabled")', salvar)

        # self.page.driver.execute_script('arguments[0].class = "cke_button cke_button__save cke_button_off"', salvar)

        # salvar.click()

        # sleep(5)

        # selfpage.fechar()

    # def concluir_processo(self):
    #
    #     excluir = self._get_acoes().get("Concluir Processo").strip()
    #
    #     assert (
    #         excluir is not None
    #     ), "A ação 'Concluir Processo não foi armazenada, verfique as ações do Processo"
    #
    #     # Switch to central frame
    #     self.page.driver.switch_to_frame("ifrVisualizacao")
    #
    #     try:
    #
    #         self.page.driver.execute_script(excluir)
    #
    #     except JavascriptException as e:
    #
    #         print("One exception was catched: {}".format(repr(e)))
    #
    #         alert = self.page.alert_is_present()
    #
    #         if alert:
    #             alert.accept()
    #
    #         self.page.driver.switch_to_default_content()


def armazena_bloco(sei, numero):
    if sei.get_title() != config.Bloco.TITLE + " " + str(numero):
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

        if pode_expedir(p):
            proc = p["processo"].a.string

            num_doc = p["documento"].a.string

            link = sei.go(p["processo"].a.attrs["href"])

            (bloco_window, proc_window) = Page.nav_link_to_new_win(sei.driver, link)

            processo = Processo(sei.driver, proc_window)

            processo.expedir_oficio(num_doc)
