#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esta é a classe principal que adiciona funcionalidades ao webdriver do Selenium.

As demais classes inicialmente herdavam esta, no entanto futuramente deverá ser alterado como esta sendo um Atributo de Classe 
@author: Ronaldo da Silva Alves Batista
"""

from contextlib import contextmanager
from typing import Any, Union, Dict, List, Tuple, Callable, Sequence, Optional
from dataclasses import dataclass

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
from selenium import webdriver

Browser = webdriver


# Base Class
@dataclass
class Page:
    """This Base class implements common navigation methods on any page.
    Adds useful features to Selenium navigation.
    Args:
        driver (selenium.webdriver): Selenium Browser Instance - Firefox, Chrome, Edge etc.

    """

    driver: Browser = None
    driver_path: Any = None

    if driver is not None:
        self.driver = driver

    else:
        assert driver_path is not None, "You need to inform the path to webdriver"
        self.driver = webdriver.Firefox(firefox_binary=driver_path)

    def restart_driver(self, driver: Browser = None) -> None:
        """Restarts webdriver instance
        
        Args:
            driver (selenium.webdriver): Selenium Browser Instance - Firefox, Chrome, Edge etc.
        """

        self.__init__(driver)

    def fechar(self) -> None:
        """Fecha a instância atual do browser
        
        Returns:
            None
        """
        self.driver.close()

    def _clicar(
        self, btn_id: Tuple, silent: bool = True, timeout: int = 10
    ) -> Union[str,]:
        """Clica no botão ou link definido pelo elemento btn_id
        
        Args:
            btn_id (tuple): localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
            silencioso (bool, optional): Defaults to True. Se verdadeiro confirma o pop-up após o clique no botão
            timeout (int, optional): Defaults to 10. tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
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
            if silent:
                text = alerta.text
                alerta.accept()
                return text
            else:
                return alerta
        else:
            return None

    def _atualizar_elemento(
        self, elem_id: Tuple, dado: str, timeout: int = 10
    ) -> Optional[str]:
        """Limpa o conteúdo do form definido pelo `elem_id` e insere o conteúdo dado
        
        Args:
            elem_id (tuple): localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
            dado (str): conteúdo a ser inserido no form definido pelo elem_id
            timeout (int, optional): Defaults to 10. tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        """

        try:

            elem = self.wait_for_element(elem_id, timeout=timeout)

            elem.clear()

            elem.send_keys(dado)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            return repr(e)

    def _selecionar_por_texto(
        self, select_id: Tuple, text: str, timeout: int = 10
    ) -> Optional[str]:
        """

        :param select_id: localizador da página html que define um Select (menu drop-down):
                          (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param text: texto da opção do menu a ser selecionada
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None
        Seleciona o menu drop-down definido pela tupla select_id e escolhe a opção cujo texto de amostra é igual a text
        """

        try:

            lista = Select(self.wait_for_element_to_click(select_id, timeout=timeout))

            lista.select_by_visible_text(text)

        except NoSuchElementException as e:
            raise ValueError(f"Não existe a opção {text} no Menu mencionado") from e

        # except UnexpectedAlertPresentException as e:

        alerta = self.alert_is_present(timeout=timeout)

        if alerta:
            txt = alerta.text
            alerta.accept()
            return txt

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

    def elem_is_visible(self, *locator: Tuple, timeout: int = 10):
        """
        Check is locator is visible on page given the timeout

        Args: Instance of object and a locator defined on locators module

        Return: True if locator is visible, False o.w.
        """
        try:

            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(locator)
            )

        except TimeoutException:
            return False

        return True

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url()

    def hover(self, *locator: Tuple):
        element = self.wait_for_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def check_element_exists(self, *locator: Tuple, timeout: int = 10):
        try:
            self.wait_for_element_to_be_visible(*locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_to_be_visible(self, *locator: Tuple, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(*locator)
        )

    def wait_for_element(self, *locator: Tuple, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(*locator)
        )

    def wait_for_element_to_click(self, *locator: Tuple, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(*locator)
        )

    def wait_for_new_window(self, windows: Sequence, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            ec.new_window_is_opened(windows)
        )

    # TODO: generalize this method
    def nav_elem_to_new_win(self, elem: Tuple):
        """ Abre o link `elem` em uma nova janela e retorna o foco para esta nova janela 
            Assume que há um link presente no elemento html `elem`.
            Se usado dentro do gerenciador de contexto `self._navega_nova_janela`
            o foco é retornado para a janela original após a saída do contexto
            Args:
               elem: elemento html com link navegável
            Return:
                None
        """
        if not self.check_element_exists(elem):
            raise NoSuchElementException(
                f"O elemento html {elem} não foi encontrado na página atual"
            )

        # Abre link no elem em uma nova janela
        elem.send_keys(Keys.SHIFT + Keys.RETURN)

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to_window(windows[-1])

        return None

    # TODO: generalize this method
    def nav_link_to_new_win(self, link: str):
        """ Abre o link `link` em uma nova janela e retorna o foco para esta nova janela 
            Assume que há um link presente no elemento html `elem`.
            Se usado dentro do gerenciador de contexto `self._navega_nova_janela`
            o foco é retornado para a janela original após a saída do contexto
            Args:
               link: elemento html com link navegável
            Return:
                None
        """
        self.driver.execute_script("window.open()")

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to.window(windows[-1])

        self.driver.get(link)

        return None

    def _click_button_new_win(
        self, btn_id: Tuple, silencioso: bool = True, timeout: int = 10
    ):
        """

        :param btn_id: localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param silencioso: se verdadeiro confirma o pop-up após o clique no botão
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None

            Método auxiliar para clicar num elemento da página que abre uma nova janela. Muda o foco para
            a nova janela.
        """

        self._clicar(btn_id=btn_id, silent=silencioso, timeout=timeout)

        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to.window(windows[-1])
