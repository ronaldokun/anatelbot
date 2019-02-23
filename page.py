#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:44:15 2017

@author: ronaldo
"""

from contextlib import contextmanager
from typing import Dict, List

import selenium
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
    ElementClickInterceptedException,
    WebDriverException,
)

# Utilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import *


# Base Class
class Page(object):
    # noinspection SpellCheckingInspection
    """Esta classe Base implementa métodos de navegação comum em qualquer página

    """

    def __init__(self, driver):
        """Initializes the webdriver
        :param driver: Selenium webdriver instance
        :type driver: selenium.webdriver                

        """

        self.driver = driver

    def reiniciar_driver(self, driver):
        """
        :param driver: selenium.webdriver
        :return: None

                 Reinicia a instância do webdriver
        """
        self.__init__(driver)

    def __enter__(self):
        """ Implementation class """
        return self

    def close(self):
        """

        :return: None

        Fecha a instância atual do browser
        """
        self.driver.close()

    def _click_button(self, btn_id: tuple, silencioso: bool = True, timeout: int = 10):
        """

        :param btn_id: localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param silencioso: se verdadeiro confirma o pop-up após o clique no botão
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None

        Clica no botão ou link definido pelo elemento btn_id
        """

        try:

            botão = self.wait_for_element_to_click(btn_id, timeout=timeout)

            botão.click()

        except NoSuchElementException as e:

            print(repr(e))

        except ElementClickInterceptedException:

            # noinspection PyUnboundLocalVariable
            self.driver.execute_script("arguments[0].click();", botão)

        alerta = self.alert_is_present(timeout=timeout)

        if alerta:

            text = alerta.text

            if silencioso:
                alerta.accept()

            return str(text)

        else:

            return None

    def _atualizar_elemento(self, elem_id: tuple, dado: str, timeout: int = 10):
        """

        :param elem_id: localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param dado: conteúdo a ser inserido no form definido pelo elem_id
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None
        Limpa o conteúdo do form definido pelo `elem_id` e insere o conteúdo dado
        """

        try:

            elem = self.wait_for_element(elem_id, timeout=timeout)

            elem.clear()

            elem.send_keys(dado)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            return repr(e)

    def _selecionar_por_texto(self, select_id, text, timeout: int = 10):
        """

        :param select_id: localizador da página html que define um Select (menu drop-down):
                          (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param text: texto da opção do menu a ser selecionada
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None
        Seleciona o menu drop-down definido pela tupla select_id e escolhe a opção cujo texto de amostra é igual a text
        """

        try:

            lista = Select(self.wait_for_element_to_click(select_id))

            lista.select_by_visible_text(text)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            alerta = self.alert_is_present(timeout=timeout)

            if alerta:
                alerta.accept()

            print(repr(e))

    @contextmanager
    def _navega_nova_janela(self, main=None):
        """

        :param main: Caso seja fornecida uma instância do webdriver
        :return:
        """

        if main is None:
            main = self.driver.current_window_handle

        try:
            # yield the state with the main window
            yield
            # inside the context manager there is a window switch

        finally:
            # return to the main window
            self.driver.switch_to.window(main)

    @contextmanager
    def wait_for_page_load(self, timeout: int = 10):
        """ Only used when navigating between Pages with different titles"""
        old_page = self.driver.find_element_by_tag_name("title")

        yield

        WebDriverWait(self.driver, timeout).until(ec.staleness_of(old_page))

    def alert_is_present(self, timeout: int = 10):

        try:

            alert = WebDriverWait(self.driver, timeout).until(ec.alert_is_present())

        except (TimeoutException, WebDriverException):

            return False

        return alert

    def elem_is_visible(self, *locator, timeout: int = 10):
        """
        Check is locator is visible on page given the timeout

        Args: Instance of object and a locator defined on locators module

        Return: True if locator is visible, False o.w.
        """
        try:

            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(*locator)
            )

        except TimeoutException:
            return False

        return True

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url()

    def hover(self, *locator):
        element = self.wait_for_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def check_element_exists(self, *locator, timeout: int = 10):
        try:
            self.wait_for_element_to_be_visible(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_to_be_visible(self, *locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(*locator)
        )

    def wait_for_element(self, *locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(*locator)
        )

    def wait_for_element_to_click(self, *locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(*locator)
        )

    def wait_for_new_window(self, windows, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.new_window_is_opened(windows)
        )

    def nav_elem_to_new_win(self, elem):
        """ navigate the link present in element to a new window
            focus the page on the new window
            Assumes the is a link present in the html element 'elem'
            Args:
               elem: html element with navigable link
            Return:
                tuple with both webdriver windows objects
                with the browser focused on the new one.
        """
        # Guarda janela principal
        main_window = self.driver.current_window_handle

        # Abre link no elem em uma nova janela
        elem.send_keys(Keys.SHIFT + Keys.RETURN)

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to_window(windows[-1])

        return main_window, windows[-1]

    def nav_link_to_new_win(self, link):

        # Guarda janela principal
        main_window = self.driver.current_window_handle

        self.driver.execute_script("window.open()")

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to.window(windows[-1])

        self.driver.get(link)

        return main_window, windows[-1]

    def _click_button_new_win(
        self, btn_id: tuple, silencioso: bool = True, timeout: int = 10
    ):
        """

        :param btn_id: localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param silencioso: se verdadeiro confirma o pop-up após o clique no botão
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None

            Método auxiliar para clicar num elemento da página que abre uma nova janela. Muda o foco para
            a nova janela.
        """

        self._click_button(btn_id=btn_id, silencioso=silencioso, timeout=timeout)

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to.window(windows[-1])
