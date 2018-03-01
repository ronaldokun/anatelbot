#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:44:15 2017

@author: ronaldo
"""

from contextlib import contextmanager

import base


# Base Class
class Page(object):
    """
    This Base Class implements common Seslenium Webdriver
    navigation methods
    """

    timeout = 30

    def __init__(self, driver):
        """ Initializes the webdriver and the timeout"""
        try:

            self.driver = driver

        except TypeError:

            print("The object {0} must be of type{1}".format(driver, type(base.webdriver)))

    def __enter__(self):
        """ Implementation class """
        return self

    def close(self):
        """ Basic implementation class"""
        self.driver.close()

    @contextmanager
    def wait_for_page_load(self, timeout=timeout):
        """ Only used when navigating between Pages with different titles"""
        old_page = self.driver.find_element_by_tag_name('title')
        yield
        base.WebDriverWait(self.driver, timeout).until(
            base.ec.staleness_of(old_page))

    def alert_is_present(self, timeout=timeout):

        try:

            alert = base.WebDriverWait(self.driver, timeout).until(
                base.ec.alert_is_present())

        except (base.TimeoutException, base.WebDriverException):

            return False

        return alert

    def elem_is_visible(self, *locator, timeout=timeout):
        """
        Check is locator is visible on page given the timeout

        Args: Instance of object and a locator defined on locators module

        Return: True if locator is visible, False o.w.
        """
        try:

            base.WebDriverWait(self.driver, timeout).until(
                base.ec.visibility_of_element_located(*locator))

        except base.TimeoutException:

            return False

        return True

    def find_element(self, *locator):
        return self.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url()

    def hover(self, *locator):
        element = self.find_element(*locator)
        hover = base.ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def check_element_exists(self, *locator):
        try:
            self.wait_for_element(*locator)
        except base.TimeoutException:
            return False
        return True

    def wait_for_element_to_be_visible(self, *locator, timeout=timeout):
        return base.WebDriverWait(self.driver, timeout).until(
            base.ec.visibility_of_element_located(*locator))

    def wait_for_element(self, *locator, timeout=timeout):
        return base.WebDriverWait(self.driver, timeout).until(
            base.ec.presence_of_element_located(*locator))

    def wait_for_element_to_click(self, *locator, timeout=timeout):
        return base.WebDriverWait(self.driver, timeout).until(
            base.ec.element_to_be_clickable(*locator))

    def wait_for_new_window(self, timeout=timeout):
        return base.WebDriverWait(self.driver, timeout).until(
            base.ec.number_of_windows_to_be(2))

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
