#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:44:15 2017

@author: ronaldo
"""

from contextlib import contextmanager

from __main__ import *

# Base Class
class Page(object):
    """
    This Base Class implements common Selenium Webdriver
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
