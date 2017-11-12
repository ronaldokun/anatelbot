# -*- coding: utf-8 -*-

# python modules imports
import os

import re

import pandas as pd

from datetime import datetime as dt
from datetime import time

# HTML PARSER
from bs4 import BeautifulSoup as soup

# INITIALIZE DRIVER
from selenium import webdriver

# WAIT AND CONDITIONS METHODS
# available since 2.26.0
from selenium.webdriver.support.ui import Select

# Exceptions
from selenium.common.exceptions import TimeoutException


# METHODS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from locators import Login, Base, LatMenu, \
    Main, ListaBlocos, Bloco, Processo, Envio


# Personal Files
from base import Page

import sei_functions as ft


def login_SEI(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    page = Page(driver)
    page.driver.get(Login.URL)
    page.driver.maximize_window()

    usuario = page.wait_for_element_to_click(Login.LOGIN)
    senha = page.wait_for_element_to_click(Login.SENHA)

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
            ver_todos = self.wait_for_element_to_click(Main.FILTROATRIBUICAO)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                Main.TIPOVISUALIZACAO)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def isPaginaInicial(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == 'SEI - Controle de Processos'

    def go_to_initial_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        self.wait_for_element_to_click(
            Base.INITIALPAGE).click()

    def exibir_menu_lateral(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(Base.EXIBIRMENU)

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

        contador = Select(self.wait_for_element(Main.CONTADOR))

        pages = [pag.text for pag in contador.options]

        for pag in pages:

            # One simple repetition to avoid more complex code
            contador = Select(self.wait_for_element(Main.CONTADOR))
            contador.select_by_visible_text(pag)
            html_sei = soup(self.driver.page_source, "lxml")
            self.processos += html_sei("tr", {"class": 'infraTrClara'})

        # percorre a lista de processos
        # cada linha corresponde a uma tag mãe 'tr'
        # substituimos a tag mãe por uma lista das tags filhas 'tag.contents', descartando os '\n'
        # a função lista_to_dict_tags recebe essa lista e retorna um dicionário das tags
        self.processos = [ft.cria_tags_dict([tag for tag in line.contents
                                             if tag != '\n']) for line in self.processos]


class Blocos(Page):

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

            if ft.podeExpedir(p):

                proc = p['processo'].a.string

                num_doc = p['documento'].a.string

                link = Base.NAV_URL + p['processo'].a.attrs['href']

                (bloco_window, proc_window) = ft.navigate_link_to_new_window(
                    self.driver, link)

                self.expedir_oficio(proc, num_doc, link)


class Processo(Page):

    pass  # TODO: Guardar processos em detalhes
