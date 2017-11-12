# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import datetime as dt

from selenium import webdriver

from modules.base import Page

from modules.locators import Boleto

from selenium.webdriver.common.keys import Keys


def last_day_of_month():
    """ Use datetime module and manipulation to return the last day
        of the current month, it's doesn't matter which.
        Return: Last day of current month, valid for any month
    """
    any_day = dt.date.today()

    next_month = any_day.replace(
        day=28) + dt.timedelta(days=4)  # this will never fail
    # this will always result in the last day of the month
    date = next_month - dt.timedelta(days=next_month.day)

    date = dt.datetime.strftime("%d%m%y")

    return date


def imprime_boleto(page, ident, id_type='cpf'):
    """ This function receives a webdriver object, navigates it to the
    Boleto page, inserts the identification 'ident' in the proper
    field and commands the print of the boleto
    """
    # navigate to page
    page.driver.get(Boleto.URL)

    if id_type == 'cpf':

        cpf = page.wait_for_element_to_click(Boleto.B_CPF)

        cpf.click()

        elem = page.wait_for_element_to_click(Boleto.INPUT_CPF)

    else:

        fistel = page.wait_for_element_to_click(Boleto.B_FISTEL)

        fistel.click()

        elem = page.wait_for_element_to_click(Boleto.INPUT_FISTEL)

    elem.clear()

    elem.send_keys(ident)

    date = page.wait_for_element_to_click(Boleto.INPUT_DATA)

    date.clear()

    date.send_keys(last_day_of_month() + Keys.RETURN)

    # page.wait_for_element_to_click(Boleto.BUT_CONF).click()

    try:

        marcar = page.wait_for_element_to_click(Boleto.MRK_TODOS)

        marcar.click()

        imprimir = page.wait_for_element_to_click(Boleto.PRINT)

        imprimir.click()

    except:

        return False

    return True

# dtype_dic = { 'CPF' : str, 'FISTEL' : str}

# df = pd.read_csv('ie/cassacao.csv', dtype=dtype_dic)


