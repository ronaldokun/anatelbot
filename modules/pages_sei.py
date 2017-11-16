# -*- coding: utf-8 -*-

# python modules imports
import os
import re
from datetime import datetime as dt
from datetime import time

from getpass import getuser, getpass

import pandas as pd
from bs4 import BeautifulSoup as soup
# INITIALIZE DRIVER
from selenium import webdriver
# Exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# METHODS
from selenium.webdriver.common.keys import Keys
# WAIT AND CONDITIONS METHODS
# available since 2.26.0
from selenium.webdriver.support.ui import Select

import sei_functions as ft
# Personal Files
from base import Page
import locators  as loc

def login_SEI(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    page = Page(driver)
    page.driver.get(loc.Login.URL)
    page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(loc.Login.LOG)
    senha = page.wait_for_element_to_click(loc.Login.PWD)

    # Clear any clutter on the form
    usuario.clear()
    usuario.send_keys(usr)

    senha.clear()
    senha.send_keys(pwd)

    # Hit Enter
    senha.send_keys(Keys.RETURN)

    return SEI(page.driver)


class SEI(Page):
    """
    Esta subclasse da classe Page define métodos de execução de ações na 
    página principal do SEI e de resgate de informações
    """

    processos = []

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
        self.processos = []

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
            self.processos += html_sei("tr", {"class": 'infraTrClara'})

        # percorre a lista de processos
        # cada linha corresponde a uma tag mãe 'tr'
        # substituimos a tag mãe por uma lista das tags filhas 
        # 'tag.contents', descartando os '\n'
        # a função lista_to_dict_tags recebe essa lista e 
        # retorna um dicionário das tags
        self.processos = [ft.armazena_tags(
                         [tag for tag in line.contents if tag != '\n']) 
                         for line in self.processos]
        
        self.processos = {p['processo'].string : p for p in self.processos}
        
        


class Blocos(Page):

    def exibir_bloco(self, numero):

        if self.get_title() != loc.Blocos.TITLE:
            self.go_to_blocos()

        try:
            self.wait_for_element((By.LINK_TEXT, str(numero))).click()

        except:
            print("O Bloco de Assinatura informado não existe ou está \
                  concluído!")

    def armazena_bloco(self, numero):

        if self.get_title() != loc.Bloco.TITLE + " " + str(numero):

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

            # proc["expedido"] = False

            lista_processos.append(proc)

        return lista_processos

    def expedir_bloco(self, numero):

        processos = self.armazena_bloco(numero)

        for p in processos:

#            if p['expedido']:
#
#                print("Processo %s já foi expedido!\n", p['processo'].a.string)
#                next

            if ft.podeExpedir(p):

                proc = p['processo'].a.string

                num_doc = p['documento'].a.string

                link = loc.Base.URL + p['processo'].a.attrs['href']

                (bloco_window, proc_window) = ft.nav_link_to_new_win(
                    self.driver, link)
                
                processo = Processo(self.driver, proc_window)

                processo.expedir_oficio(proc, num_doc, link)


class Processo(Page):
    
    tree = {}
    
    def __init__(self, driver, tags):        
        super().__init__(driver)
        self.tags = tags
        
    def fecha_processo_atual(self):        
        
        self.driver.close()
        
    def cria_processo(self, tipo, desc='', inter='', nivel = 'público'):
        
        tipo = str(tipo)
        
        assert tipo in loc.Tipos.PROCS,\
        print("O tipo de processo digitado {0}, não é válido".format(str(tipo)))
        
        select = Select(self.wait_for_element(loc.Tipos.SL_TIP_PROC))
        
        select.select_by_visible_text(tipo)
        
        if desc:
            
            espec = self.wait_for_element(loc.Processo.ESPEC)
            
            espec.send_keys(desc)
            
        if inter:
            
            self.cadastrar_interessado(inter)
            
        
    def consultar_contato(self, nome):
        
        pass
    
    def cadastrar_interessado(self, nome, tipo='pf', dados):
    
        pass

            
            
        
    
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

        with self.wait_for_page_load():
            
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

        # fecha a janela processo
        # self.driver.close()



        
    def expedir_oficio(self, num_doc):

        info = self.info_oficio(num_doc)

        # self.driver.switch_to_window(self.window)

        buttons = self.acoes_oficio()

        self.atualiza_andamento(buttons, info)

        self.enviar_processo_sede(buttons)

        # self.driver.switch_to_window(main_window)
        
        
def main():
    
    login = getuser()
    
    senha = getpass(prompt="Senha: ")
        
    driver = webdriver.Chrome()
    
    sei = login_SEI(driver, login, senha)
    
    return sei

#if __name__ == "__main__":
    
 #   main()
    
sei = main()         
