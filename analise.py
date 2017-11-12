# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import pandas as pd

from selenium import webdriver

from modules.base import Page

from modules.functions import imprime_boleto

def imprime_boleto(Page, ident, id_type='cpf'):
        """ This function receives a Page object, navigates it to the 
        Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """
        # navigate to page
        Page.driver.get(Boleto.URL)

#dtype_dic = { 'CPF' : str, 'FISTEL' : str}

#df = pd.read_csv('ie/cassacao.csv', dtype=dtype_dic)

driver = webdriver.Ie()

ie = Page(driver)
