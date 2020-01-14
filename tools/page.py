#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Esta é a classe principal que adiciona funcionalidades ao webdriver do Selenium.

Ela é um atributo de classe das demais classes específicas.
@author: Ronaldo da Silva Alves Batista
"""
# Standard Lib Imports
from contextlib import contextmanager
from typing import Any, Optional, Sequence, Tuple, Union

# Third-Parties imports
import selenium
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Local application imports
from .functions import get_browser

Elem = Tuple[Any, str]


# Base Class
# noinspection NonAsciiCharacters,SpellCheckingInspection
class Page:
    """This Base class implements common navigation methods on any page.
    Adds useful features to Selenium navigation.
    Args:
        driver (selenium.webdriver): Selenium Browser Instance - Firefox, Chrome, Edge etc.

    """

    timeout: int = 10

    def __init__(self, driver: webdriver):
        self.driver = driver

    def restart_driver(self, **kwargs) -> None:
        """Restarts webdriver instance
        """
        self.driver = get_browser(**kwargs)

    def fechar(self) -> None:
        """Fecha a instância atual do browser
        
        Returns:
            None
        """
        self.driver.close()

    def _clicar(self, btn_id: Elem, silent: bool = True) -> Union[str, None, Any]:
        """Clica no botão ou link definido pelo elemento btn_id

        Args:
            btn_id (tuple): localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
            silent (bool, optional): Defaults to True. Se verdadeiro confirma o pop-up após o clique no botão
        """

        try:

            botão = self.wait_for_element_to_click(btn_id)

            botão.click()

        except (NoSuchElementException, TimeoutException) as e:

            return e

        except ElementClickInterceptedException:

            # noinspection PyUnboundLocalVariable
            self.driver.execute_script("arguments[0].click();", botão)

        alerta = self.alert_is_present()

        if alerta:
            if silent:
                text = alerta.text
                alerta.accept()
                return text
            else:
                return alerta
        else:
            return True

    def _clicar_se_existir(
        self, btn_id: Elem, silent: bool = True
    ) -> Union[str, None, Any]:
        if self.check_element_exists(btn_id):
            return self._clicar(btn_id, silent)
        return None

    def _atualizar_elemento(self, elem_id: Elem, dado: str) -> Optional[str]:
        """Limpa o conteúdo do form definido pelo `elem_id` e insere o conteúdo dado

        Args:
            elem_id (tuple): localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
            dado (str): conteúdo a ser inserido no form definido pelo elem_id
        """

        try:

            elem = self.wait_for_element(elem_id)

            elem.clear()

            elem.send_keys(dado)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            return repr(e)

        return None

    def _selecionar_por_texto(self, select_id: Elem, text: str) -> Optional[str]:
        """

        :param select_id: localizador da página html que define um Select (menu drop-down):
                          (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param text: texto da opção do menu a ser selecionada
        :return: None
        Seleciona o menu drop-down definido pela tupla select_id e escolhe a opção cujo texto de amostra é igual a text
        """

        try:

            lista = Select(self.wait_for_element_to_click(select_id))

            lista.select_by_visible_text(text)

        except NoSuchElementException:
            print(f"Não existe a opção {text} no Menu mencionado")

        alerta = self.alert_is_present()

        if alerta:
            txt = alerta.text
            alerta.accept()
            return txt

        return None

    @contextmanager
    def _go_new_win(self, main=None) -> None:
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
    def wait_for_page_load(self):
        """ Only used when navigating between Pages with different titles"""
        old_page = self.driver.find_element_by_tag_name("title")

        yield

        WebDriverWait(self.driver, self.timeout).until(EC.staleness_of(old_page))

    def alert_is_present(self) -> Union[WebDriverWait, bool]:

        try:

            alert = WebDriverWait(self.driver, self.timeout).until(
                EC.alert_is_present()
            )

        except (TimeoutException, WebDriverException):

            return False

        return alert

    def elem_is_visible(self, *locator: Elem):
        """
        Check is locator is visible on page given the timeout

        Args: Instance of object and a locator defined on locators module

        Return: True if locator is visible, False o.w.
        """
        try:

            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )

        except TimeoutException:
            return False

        return True

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url()

    def hover(self, *locator: Elem):
        element = self.wait_for_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def check_element_exists(self, *locator: Elem):
        try:
            self.wait_for_element_to_be_visible(*locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_to_be_visible(self, *locator: Elem):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(*locator)
        )

    def wait_for_element(self, *locator: Elem):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(*locator)
        )

    def wait_for_element_to_click(self, *locator: Elem):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(*locator)
        )

    def wait_for_new_window(self, windows: Optional[Sequence]=None):
        """

        Args:
            windows (Sequence):
        """
        if windows is None:
            windows = self.driver.window_handles

        return WebDriverWait(self.driver, self.timeout).until(
            EC.new_window_is_opened(windows)
        )

    @contextmanager
    def switch_to_win_opened(self):

        yield

        windows = self.driver.window_handles

        self.driver.switch_to.window(windows[-1])

    @_go_new_win
    def nav_elem_to_new_win(self, elem):
        """ Abre o link `elem` em uma nova janela e retorna o foco para esta nova janela
            Assume que há um link presente no elemento html `elem`.
            Se usado dentro do gerenciador de contexto `self._go_new_win`
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

    @_go_new_win
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

        self.driver.get(link)

        return None

    @contextmanager
    def _clica_abre_nova_janela(self, btn_id: Elem):
        """               

        :param btn_id: localizador da página html: (id, conteúdo), (title, conteúdo), (link_text, conteúdo)
        :param silent: se verdadeiro confirma o pop-up após o clique no botão
        :param timeout: tempo de espera fornecido aos métodos no carregamento/atualização dos elementos da página
        :return: None

            Método auxiliar para clicar num elemento da página que abre uma nova janela. Muda o foco para
            a nova janela.
        """
        with self._go_new_win():
            with self.switch_to_win_opened():
                self._clicar(btn_id=btn_id)
            print(self.driver.current_window_handle)
            yield
