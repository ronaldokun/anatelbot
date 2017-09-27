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


class Base(Page):
    """ This class is a Page class with additional methods to be executed 
        on elements present in the Header Frame and Menu Frame in SEI. 
        Those Headers are present in all Pages inside SEI, e.g., since is 
        logged in
    """

    def isPaginaInicial(self):
        return self.get_title() == 'SEI - Controle de Processos'

    def go_to_initial_page(self):
        self.find_element(Base.INITIALPAGE).click()

        menu = self.find_element(Base.EXIBIRMENU)

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()
            

class PagInicial(Base):

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

    def lista_processos(self):

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
    
#TODO: Guardar processos em detalhes
