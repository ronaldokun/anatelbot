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
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0


# WAIT AND CONDITIONS METHODS
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# METHODS
from selenium.webdriver.common.keys import Keys

# EXCEPTIONS
from selenium.common.exceptions import \
    TimeoutException, \
    ElementNotVisibleException, \
    NoSuchElementException

from locators import *
from base import Page


class LoginPage(Page):
   
      
    def login(self, usr, pwd):
        """
        with self.driver, navigate to url
        make login and return and instance of browser"""
               
        self.driver.get(URL)
        self.driver.maximize_window()


        usuario = self.wait_for_element_to_click(LOGIN)
        senha = self.wait_for_element_to_click(SENHA)
        
        # Clear any clutter on the form
        usuario.clear()
        usuario.send_keys(usr)

        senha.clear()
        senha.send_keys(pwd)

        # Hit Enter
        senha.send_keys(Keys.RETURN)

        
        return Sei(self.driver)    


class Sei(Page):
    
    """
    This class is a subclass of page, this class is a logged page
    """
        
    def expand_visual(self):
        # example use
        with self.wait_for_page_load():
    
            try:
                ver_todos_processos = self.wait_for_element_to_click(
                        FILTROATRIBUICAO)
    
                if ver_todos_processos.text == 'Ver todos os processos':
                    ver_todos_processos.click()
            except:
                
                print("Ocorreu algum erro na Visualização dos Processos")
    
            # Verifica se está na visualização detalhada senão muda para ela
            try:
                visualizacao_detalhada = self.wait_for_element_to_click(
                        TIPOVISUALIZACAO)
    
                if visualizacao_detalhada.text == 'Visualização detalhada':
                    visualizacao_detalhada.click()
    
            except:
                print("Falha na visualização detalhada dos processos")
                
        
            
    def isPaginaInicial(self):
        return self.get_title() == 'SEI - Controle de Processos'

    def go_to_initial_page(self):
        
        self.wait_for_element_to_click(
                INITIALPAGE).click()
    
    
    def exibir_menu_lateral(self):
        
        if not self.isPaginaInicial():
            self.go_to_initial_page()
            
        menu = self.find_element(EXIBIRMENU)
        
        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()
        

    def lista_processos(self):
        
        processos = []
                
        if not self.isPaginaInicial():
            self.go_to_initial_page()
            
        contador = Select(self.find_element(CONTADOR))
                
        pages = [pag.text for pag in contador.options]
                
        for pag in pages:        
            
            contador = Select(self.find_element(CONTADOR))
            contador.select_by_visible_text(pag)
            html_sei = soup(driver.page_source, "lxml")
            processos += html_sei("tr", {"class":'infraTrClara'})
            
            
        return processos
    
    
    def go_to_blocos(self):
        self.exibir_menu_lateral()
        self.find_element(BLOCOASS).click()
        
    def exibir_bloco(self, numero):
        
        if self.get_title() != LISTA_BLS_TITLE:
            self.go_to_blocos()
            
        try:
            self.find_element((By.LINK_TEXT, str(numero))).click()
            
        except NoSuchElementException:
            print("O Bloco de Assinatura informado não existe ou está \
                  concluído!")
            
    def armazena_bloco(self,numero):
        
        if self.get_title() != BLOCO_TITLE + " " + str(numero):
            
            self.exibir_bloco(numero)
            
        html_bloco = soup(driver.page_source, "lxml")
        linhas = html_bloco("tr", {"class":'infraTrClara'})
        
        chaves = ['checkbox', 'seq', "processo", 'documento', 'data', 'tipo', \
                  'assinatura', 'anotacoes', 'acoes']
                
        proc = {k:None for k in chaves}
                                
        lista_processos = []
        
                
        for linha in linhas:
            
            col = [v for v in linha.contents if v != '\n']
            
            assert len(col) == len(chaves)
            
            for k,v in zip(chaves, col):
                
                proc[k] = v
                        
            lista_processos.append(proc)
            
        return lista_processos
    
            
    def isBlocoReady(self, numero):
        
        pass
            
            
            
            
            
            
        
        
            
        
        
        
            
    def expedir_bloco(self, numero):
        
        if self.get_title() != BLOCO_TITLE + " " + str(numero):
            
            self.exibir_bloco(numero)
            
        html_bloco = soup(driver.page_source, "lxml")
        processos = html_bloco("tr", {"class":'infraTrClara'})
            
        
      
        
        


   
    

        
        
    
        
    
                
        
                
driver = webdriver.Chrome()

sei = LoginPage(driver).login('rsilva', 'Savorthemom3nts')

sei.go_to_blocos()

#sei.exibir_bloco(68049)

bloco = sei.armazena_bloco(68049)

#sei.expand_visual()

#processos = sei.lista_processos()

#sei.exibir_menu_lateral()

        
    





