# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:55:01 2017

@author: rsilva
"""

# HTML PARSER
from bs4 import BeautifulSoup as soup

# INITIALIZE DRIVER
from selenium import webdriver

# WAIT AND CONDITIONS METHODS
# available since 2.26.0
from selenium.webdriver.support.ui import Select

# METHODS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from locators import Login, Base, LatMenu, \
    Main, ListaBlocos, Bloco, Processo, Envio


from base import Page


def podeExpedir(p):

    t1 = p['processo'].find_all('a', class_="protocoloAberto")

    t2 = p['tipo'].find_all(string="Ofício")

    t3 = p['assinatura'].find_all(string=re.compile("Coordenador"))

    t4 = p['assinatura'].find_all(string=re.compile("Gerente"))

    return bool(t1) and bool(t2) and (bool(t3) or bool(t4))


def navigate_elem_to_new_window(driver, elem):
    """ Receive an instance of Page, navigate the link to a new window

        focus the driver in the new window

        return the main window and the driver focused on new window

        Assumes link is in page
    """
    # Guarda janela principal
    main_window = driver.current_window_handle

    # Abre link no elem em uma nova janela
    elem.send_keys(Keys.SHIFT + Keys.RETURN)

    # Guarda as janelas do navegador presentes
    windows = driver.window_handles

    # Troca o foco do navegador
    driver.switch_to_window(windows[-1])

    return (main_window, windows[-1])


def navigate_link_to_new_window(driver, link):

    # Guarda janela principal
    main_window = driver.current_window_handle

    # Abre link no elem em uma nova janela
    # body = self.driver.find_element_by_tag_name('body')

    # body.send_keys(Keys.CONTROL + 'n')

    driver.execute_script("window.open()")
    # Guarda as janelas do navegador presentes
    windows = driver.window_handles

    # Troca o foco do navegador
    driver.switch_to_window(windows[-1])

    driver.get(link)

    return (main_window, windows[-1])


class BasePage(Page):
    """ This class is a Page class with additional methods to be executed 
        on elements present in the Header Frame and Menu Frame in SEI. 
        Those Headers are present in all Pages inside SEI, e.g., since is 
        logged in
    """

    def isPaginaInicial(self):
        return self.get_title() == 'SEI - Controle de Processos'

    def go_to_initial_page(self):
        self.wait_for_element_to_click(Base.INITIALPAGE).click()

    def exibir_menu_lateral(self):

        menu = self.find_element(Base.EXIBIRMENU)

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()

    def go_to_blocos(self):
        self.exibir_menu_lateral()
        self.wait_for_element(LatMenu.BLOCOASS).click()


class Bloco(BasePage):

    def exibir_bloco(self, numero):

        if self.get_title() != ListaBlocos.TITLE:
            self.go_to_blocos()

        try:
            self.wait_for_element((By.LINK_TEXT, str(numero))).click()

        except:
            print("O Bloco de Assinatura informado não existe ou está \
                  concluído!")

    def armazena_bloco(self, numero):

        if self.get_title() != Bloco.TITLE + " " + str(numero):

            self.exibir_bloco(numero)

        html_bloco = soup(self.driver.page_source, "lxml")
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

            proc["expedido"] = False

            lista_processos.append(proc)

        return lista_processos

    def expedir_bloco(self, numero):

        processos = self.armazena_bloco(numero)

        for p in processos:

            if p['expedido']:

                print("Processo %s já foi expedido!\n", p['processo'].a.string)
                next

            if podeExpedir(p):

                proc = p['processo'].a.string

                num_doc = p['documento'].a.string

                link = Base.NAV_URL + p['processo'].a.attrs['href']

                (bloco_window, proc_window) = navigate_link_to_new_window(
                    self.driver, link)

                self.expedir_oficio(proc, num_doc, link)


class PagInicial(BasePage):

    """
    This class is a subclass of page, this class is a logged page
    """

    def expand_visual(self):

        ver_todos_processos = self.wait_for_element_to_click(
            Main.FILTROATRIBUICAO)
        # Checa se a visualização está restrita aos processos atribuidos ao
        # login
        if ver_todos_processos.text == 'Ver todos os processos':
            ver_todos_processos.click()

        # Verifica se está na visualização detalhada senão muda para ela
        visualizacao_detalhada = self.wait_for_element_to_click(
            Main.TIPOVISUALIZACAO)

        if visualizacao_detalhada.text == 'Visualização detalhada':
            visualizacao_detalhada.click()

    def guarda_todos_processos(self):

        processos = []

        if not self.isPaginaInicial():
            self.go_to_initial_page()

        self.expand_visual()

        contador = Select(self.wait_for_element(Main.CONTADOR))

        pages = [pag.text for pag in contador.options]

        for pag in pages:

            contador = Select(self.wait_for_element(Main.CONTADOR))
            contador.select_by_visible_text(pag)
            html_sei = soup(self.driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        return processos


class ProcPage(BasePage):

    # TODO: Guardar processos em detalhes
