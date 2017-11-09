# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import os

import re

import pandas as pd

import datetime as dt

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

os.chdir('../')

# Personal Files
from locators import Boleto

from base import Page

def last_day_of_month(): 
    
    any_day = dt.date.today()
    
    next_month = any_day.replace(day=28) + dt.timedelta(days=4)  # this will never fail
    
    date = next_month - dt.timedelta(days=next_month.day)
    
    date = date.strftime("%d%m%y")
            
    return date


def imprime_boleto(page, id, type='cpf'):
    
    # navigate
    page.driver.get(Boleto.URL)
    
    if type == 'cpf':
        
        cpf = page.wait_for_element_to_click(Boleto.B_CPF)
        
        cpf.click()        
               
        elem = page.wait_for_element_to_click(Boleto.INPUT_CPF)
        
    else:
        
        fistel = page.wait_for_element_to_click(Boleto.B_FISTEL)
        
        fistel.click()
        
        elem = page.wait_for_element_to_click(Boleto.INPUT_FISTEL)
        
    #elem.clear()
        
    elem.send_keys(id)
    
    date = page.wait_for_element_to_click(Boleto.INPUT_DATA)
    
    date.clear()
    
    date.send_keys(last_day_of_month())
    
    page.wait_for_element_to_click(Boleto.BUT_CONF).click()
    
    try:
        
        marcar = page.wait_for_element_to_click(Boleto.MRK_TODOS)
        
        marcar.click()
        
        imprimir = page.wait_for_element_to_click(Boleto.PRINT)
        
        imprimir.click()      
        
        
    except:
        
        print(" Entidade não devedora\n")

       
    
dtype_dic = { 'CPF' : str, 'FISTEL' : str}
    
df = pd.read_csv('ie/cassacao.csv', dtype=dtype_dic)

driver = webdriver.Ie()

ie = Page(driver)



for i in range(22,30):
    
    cpf = df['CPF'].iloc[i]
    
    imprime_boleto(ie, cpf)
    
    
    
    

    
    
    
    
    