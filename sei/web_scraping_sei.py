#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 23:14:09 2017

@author: ronaldo
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
# EXCEPTIONS
from selenium.common.exceptions import \
    NoSuchElementException

from locators import Login, Base, LatMenu, \
    Main, ListaBlocos, Bloco, Processo


from base import Page

import re


class LoginPage(Page):

    def login(self, usr, pwd):
        """
        with self.driver, navigate to url
        make login and return and instance of browser"""

        self.driver.get(Login.URL)
        self.driver.maximize_window()

        usuario = self.wait_for_element_to_click(Login.LOGIN)
        senha = self.wait_for_element_to_click(Login.SENHA)

        # Clear any clutter on the form
        usuario.clear()
        usuario.send_keys(usr)

        senha.clear()
        senha.send_keys(pwd)

        # Hit Enter
        senha.send_keys(Keys.RETURN)

        return PagInicial(self.driver)


class PagInicial(Page):

    """
    This class is a subclass of page, this class is a logged page
    """

    def expand_visual(self):
        # example use

        try:
            ver_todos_processos = self.wait_for_element_to_click(
                Main.FILTROATRIBUICAO)

            if ver_todos_processos.text == 'Ver todos os processos':
                ver_todos_processos.click()
        except:

            print("Ocorreu algum erro na Visualização dos Processos")

        # Verifica se está na visualização detalhada senão muda para ela
        try:
            visualizacao_detalhada = self.wait_for_element_to_click(
                Main.TIPOVISUALIZACAO)

            if visualizacao_detalhada.text == 'Visualização detalhada':
                visualizacao_detalhada.click()

        except:
            print("Falha na visualização detalhada dos processos")

    def isPaginaInicial(self):
        return self.get_title() == 'SEI - Controle de Processos'

    def go_to_initial_page(self):

        self.wait_for_element_to_click(
            Base.INITIALPAGE).click()

    def exibir_menu_lateral(self):

        if not self.isPaginaInicial():
            self.go_to_initial_page()

        menu = self.wait_for_element(Base.EXIBIRMENU)

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()

    def lista_processos(self):

        processos = []

        if not self.isPaginaInicial():
            self.go_to_initial_page()

        contador = Select(self.wait_for_element(Main.CONTADOR))

        pages = [pag.text for pag in contador.options]

        for pag in pages:

            contador = Select(self.wait_for_element(Main.CONTADOR))
            contador.select_by_visible_text(pag)
            html_sei = soup(driver.page_source, "lxml")
            processos += html_sei("tr", {"class": 'infraTrClara'})

        return processos

    def go_to_blocos(self):
        self.exibir_menu_lateral()
        self.wait_for_element(LatMenu.BLOCOASS).click()

    def exibir_bloco(self, numero):

        if self.get_title() != ListaBlocos.TITLE:
            self.go_to_blocos()

        try:
            self.wait_for_element((By.LINK_TEXT, str(numero))).click()

        except NoSuchElementException:
            print("O Bloco de Assinatura informado não existe ou está \
                  concluído!")

    def armazena_bloco(self, numero):

        if self.get_title() != Bloco.TITLE + " " + str(numero):

            self.exibir_bloco(numero)

        html_bloco = soup(driver.page_source, "lxml")
        linhas = html_bloco.find_all("tr", class_=['infraTrClara', 'infraTrEscura'])

        chaves = ['checkbox', 'seq', "processo", 'documento', 'data', 'tipo',
                  'assinatura', 'anotacoes', 'acoes']

        proc = {k: None for k in chaves}

        lista_processos = []

        for linha in linhas:

            cols = [v for v in linha.contents if v != "\n"]
            
            #proc['checkbox'] = linha("a", class_="infraCheckbox")
            
            #proc['seq'] = linha.
            
            assert len(chaves) == len(cols), "Verifique as linhas do bloco!"
                        
            for k, v in zip(chaves, cols):

                proc[k] = v

            lista_processos.append(proc)

        return lista_processos

    
    def navigate_elem_to_new_window(self, elem):
        """ Receive an instance of Page, navigate the link to a new window

            focus the driver in the new window

            return the main window and the driver focused on new window

            Assumes link is in page
        """
        # Guarda janela principal
        main_window = self.driver.current_window_handle

        # Abre link no elem em uma nova janela
        elem.send_keys(Keys.SHIFT + Keys.RETURN)

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to_window(windows[-1])

        return (main_window, windows[-1])

    def info_oficio(self, processo):

        # Guarda número do processo como string
        num_proc = processo['processo'].a.string

        # Guarda o link para abrir o processo
        elem = self.wait_for_element_to_click((By.LINK_TEXT, num_proc))

        (main_window, proc_window) = self.navigate_elem_to_new_window(elem)

        # TODO: Resgatar informações da arvore e chamar função alterar andamento

    def expedir_bloco(self, numero):


        processos = self.armazena_bloco(numero)

        for p in processos:

            if podeExpedir(p):

                proc = p['processo'].a.string
                num_doc = p['documento'].a.string

                # link = p['processo'].a.attrs['href']

                elem = self.wait_for_element_to_click(
                    (By.LINK_TEXT, proc))

                self.expedir_oficio(elem, proc, num_doc)

    def expedir_oficio(self, element, proc, doc):

        main_window = self.driver.current_window_handle

        element.send_keys(Keys.SHIFT + Keys.RETURN)

        windows = self.driver.window_handles

        self.driver.switch_to_window(windows[-1])

        html = soup(self.driver.page_source, "lxml").find_all('a')

        docs = html.find_all(string=re.compile(doc))

        print(docs)

        # self.driver.wait_for_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        self.driver.close()

        self.driver.switch_to.window(main_window)

    # def navigate_new_window(self, link):

        # main_window = self.driver.current_window_handle


def podeExpedir(p):

    t1 = p['processo'].find_all('a', class_="protocoloAberto")
        
    t2 = p['tipo'].find_all(string="Ofício")

    t3 = p['assinatura'].find_all(string=re.compile("Coordenador"))
    
    t4 = p['assinatura'].find_all(string=re.compile("Gerente"))
    
    return t1 and t2 and (t3 or t4)


driver = webdriver.Chrome()

sei = LoginPage(driver).login('rsilva', 'Savorthemom3nts')

sei.go_to_blocos()

# sei.exibir_bloco(68049)

bloco = sei.armazena_bloco(68757)

#sei.expedir_bloco(68757)

# sei.expand_visual()

# processos = sei.lista_processos()

# sei.exibir_menu_lateral()
