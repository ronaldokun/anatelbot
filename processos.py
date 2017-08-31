# 
# -*- coding: utf-8 -*-
    

#The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


url = "https://sei.anatel.gov.br"

#TODO Processar login pelo sys.argv


def loga_sei(browser=chrome, usr, pwd):
    
    """Initialize, make login and return and instance of browser"""

    #TODO fazer isso de uma maneira decente

    if browser == chrome:    
        # Create an instance of Chrome
        driver = webdriver.Chrome()

        # he driver.get method will navigate to a page given by the URL. 
        driver.get(url)
        
        usuario = driver.find_element_by_id("txtUsuario")
        senha = driver.find_element_by_id("pwdSenha")

        # Clear any clutter which may be on the keyboard
        usuario.clear()
        usuario.send_keys(usr)
    
        senha.clear()
        senha.send_keys(pwd)

        # Hit Enter
        senha.send_keys(Keys.RETURN)

        assert "No results found." not in driver.page_source
        
    return driver
            
usr = 'rsilva'
pwd = 'Savorthemom3nts'

driver = loga_sei(chrome, usr, pwd)

processos = []

try:
    driver.find_element_by_id("lnkRecebidosPrimeiraPaginaSuperior").click()
    
except:
    print("Página de Processos Inicial")
    


while True:
    try:
        # infraTrClara eh o frame dos processos
        processos += driver.find_elements_by_class_name('infraTrClara')
        
        #there is a counter to the next page
        counter = driver.find_element_by_id("lnkRecebidosProximaPaginaSuperior")
                
        #go to next page
        counter.click()
        
    except:
        
        break


#TODO Processar entradas de usuários    
    