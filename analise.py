# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import pandas as pd

from selenium import webdriver 

from base import Page

from modules.functions import imprime_boleto, 
      
    
dtype_dic = { 'CPF' : str, 'FISTEL' : str}
    
df = pd.read_csv('ie/cassacao.csv', dtype=dtype_dic)

driver = webdriver.Ie()

ie = Page(driver)



for i in range(22,30):
    
    cpf = df['CPF'].iloc[i]
    
    imprime_boleto(ie, cpf)
    
    
    
    

    
    
    
    
    