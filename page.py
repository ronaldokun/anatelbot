#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:44:15 2017

@author: ronaldo
"""

from contextlib import contextmanager

# Main package
import selenium.webdriver as webdriver
from selenium.common.exceptions import *
# Utilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Methods used from selenium submodules
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import *


# Exceptions


# Base Class
class Page(object):
    # noinspection SpellCheckingInspection
    """
        This Base Class implements common Selenium Webdriver
        navigation methods
        """

    timeout = 60

    def __init__(self, driver):
        """ Initializes the webdriver and the timeout"""
        #if not isinstance(type(driver), type(webdriver.)):

         #   raise ValueError("The object {0} must be of type{1}".format(type(driver), type(webdriver)))

        self.driver = driver

    def reset_driver(self, driver):
        """ Reinitializes the webdriver and the timeout"""

        self.__init__(driver)

    def __enter__(self):
        """ Implementation class """
        return self

    def close(self):
        """ Basic implementation class"""
        self.driver.close()

    def _click_button(self, btn_id, timeout=5):

        try:

            button = self.wait_for_element_to_click(btn_id, timeout=timeout)

            button.click()

        except ElementClickInterceptedException:

            #ActionChains(self.driver).move_to_element(button).click(button).perform()

            self.driver.execute_script("arguments[0].click();", button)


        except NoSuchElementException as e:

            print(repr(e))

        alert = self.alert_is_present(timeout=timeout)

        if alert:

            print(alert.text)

            alert.accept()

            return False

        else:

            return True

    def _update_elem(self, elem_id, dado, timeout=5):

        try:

            elem = self.wait_for_element(elem_id, timeout=timeout)

        except NoSuchElementException as e:

            print(e)

        elem.clear()

        elem.send_keys(dado)

    def _select_by_text(self, select_id, text, timeout=5):

        try:

            select = Select(self.wait_for_element_to_click(select_id))

            select.select_by_visible_text(text)

        except (NoSuchElementException, UnexpectedAlertPresentException) as e:

            alert = self.alert_is_present(timeout=timeout)

            if alert: alert.accept()

            print(repr(e))

    @contextmanager
    def wait_for_page_load(self, timeout=timeout):
        """ Only used when navigating between Pages with different titles"""
        old_page = self.driver.find_element_by_tag_name('title')

        yield

        WebDriverWait(self.driver, timeout).until(ec.staleness_of(old_page))

    def alert_is_present(self, timeout=timeout):

        try:

            alert = WebDriverWait(self.driver, timeout).until(ec.alert_is_present())

        except (TimeoutException, WebDriverException):

            return False

        return alert

    def elem_is_visible(self, *locator, timeout=timeout):
        """
        Check is locator is visible on page given the timeout

        Args: Instance of object and a locator defined on locators module

        Return: True if locator is visible, False o.w.
        """
        try:

            WebDriverWait(self.driver, timeout).until(
                ec.visibility_of_element_located(*locator))

        except TimeoutException:
            return False

        return True

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url()

    def hover(self, *locator):
        element = self.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def check_element_exists(self, *locator, timeout=2):
        try:
            self.wait_for_element_to_be_visible(*locator, timeout=timeout)
        except (TimeoutException, NoSuchElementException):
            return False
        return True

    def wait_for_element_to_be_visible(self, *locator, timeout=timeout):
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(*locator))

    def wait_for_element(self, *locator, timeout=timeout):
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(*locator))

    def wait_for_element_to_click(self, *locator, timeout=timeout):
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(*locator))

    def wait_for_new_window(self, windows, timeout=timeout):
        return WebDriverWait(self.driver, timeout).until(
            ec.new_window_is_opened(windows))

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

        # Abre link no elem em uma nova janela
        # body = self.driver.find_element_by_tag_name('body')

        # body.send_keys(Keys.CONTROL + 'n')

        self.driver.execute_script("window.open()")
        # Guarda as janelas do navegador presentes
        windows = self.driver.window_handles

        # Troca o foco do navegador
        self.driver.switch_to_window(windows[-1])

        self.driver.get(link)

        return main_window, windows[-1]
