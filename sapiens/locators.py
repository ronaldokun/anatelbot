#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldo
"""

from selenium.webdriver.common.by import By


class Login(object):

    URL = "https://sapiens.agu.gov.br/"

    TITLE = "SAPIENS"

    LOGIN = (By.ID, "cpffield-1018-inputEl")

    SENHA = (By.ID, "textfield-1019-inputEl")
    

class Rf(object):
    
    URL = "https://sapiens.agu.gov.br/receitafederal"
    
    IDINPUTCPF = (By.ID, "textfield-1014-inputEl")
    
    RESULTADO = (By.CLASS_NAME, "x-grid-cell-inner")
   
    CPF = (By.ID, "textfield-1014-inputEl")
    
    NAME = (By.ID, "textfield-1015-inputE1")
    
    QUADRO1 = (By.CLASS_NAME, "x-grid-cell-inner")




      
