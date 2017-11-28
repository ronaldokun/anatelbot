# -*- coding: utf-8 -*-
#!usr/bin/env python3
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import datetime as dt
import os

from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys

from modules.base import Page
import modules.locators as loc

os.chdir(r'C:\Users\rsilva\Gdrive\projects\programming\automation')


def save_page(driver, filename):

    with open(filename, 'w') as file:

        # write image
        file.write(driver.page_source)

    # driver.close()


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

    date = date.strftime("%d%m%y")

    return date


def imprime_boleto(page, ident, id_type='cpf'):
    """ This function receives a webdriver object, navigates it to the
    Boleto page, inserts the identification 'ident' in the proper
    field and commands the print of the boleto
    """
    # navigate to page
    page.driver.get(loc.Boleto.URL)

    if id_type == 'cpf':

        cpf = page.wait_for_element_to_click(loc.Boleto.B_CPF)

        cpf.click()

        elem = page.wait_for_element_to_click(loc.Boleto.INPUT_CPF)

    else:

        fistel = page.wait_for_element_to_click(loc.Boleto.B_FISTEL)

        fistel.click()

        elem = page.wait_for_element_to_click(loc.Boleto.INPUT_FISTEL)

    elem.clear()

    elem.send_keys(ident)

    date = page.wait_for_element_to_click(loc.Boleto.INPUT_DATA)

    date.clear()

    date.send_keys(last_day_of_month() + Keys.RETURN)

    # page.wait_for_element_to_click(Boleto.BUT_CONF).click()

    try:

        marcar = page.wait_for_element_to_click(loc.Boleto.MRK_TODOS)

        marcar.click()

    except:

        print("Não foi possível marcar todos os boletos")

        return False

    try:

        imprimir = page.wait_for_element_to_click(loc.Boleto.PRINT)

        imprimir.click()

    except:

        print("Não foi possível imprimir todos os boletos")

        return False

    try:

        page.wait_for_new_window()

    except:

        print("A espera pela nova janela não funcionou!")

        return False

    return True


def atualiza_cadastro(page,dados):
    
    if 'CPF' not in dados:
        
        raise ValueError("É Obrigatório informar o CPF")      
               
    if len(str(dados['CPF'])) != 11:
        
        raise ValueError("O CPF deve ter 11 caracteres!")
        
    def atualiza_campo(data, locator):
        
        data = str(data)
    
        elem = page.wait_for_element(locator)
        
        elem.clear()
        
        elem.send_keys(data)
                
    # Navigate to page
    page.driver.get(loc.Sec.Ent_Alt)
    
    cpf = page.wait_for_element_to_click(loc.Entidade.cpf)
    
    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)
       
        
    if 'Email' in dados:
        
        atualiza_campo(dados['Email'], loc.Entidade.email)
        
    btn = page.wait_for_element_to_click(loc.Entidade.bt_dados)
    
    btn.click()
            
    if 'RG' in dados:
        
        atualiza_campo(dados['RG'], loc.Entidade.rg)
        
    if 'Orgexp' in dados:
        
        atualiza_campo(dados['Orgexp'], loc.Entidade.orgexp)
        
    if 'Data de Nascimento' in dados:
        
        data = dados['Data de Nascimento']
        
        data = data.replace('-', '')
        
        atualiza_campo(data, loc.Entidade.nasc)
        
    btn = page.wait_for_element_to_click(loc.Entidade.bt_fone)
    
    btn.click()
    
        
    if 'ddd' in dados:
        
        atualiza_campo(dados['ddd'], loc.Entidade.ddd)
        
    else:
        
        ddd = '11'
        
        atualiza_campo(ddd, loc.Entidade.ddd)

        
    if 'Fone' in dados:
        
        atualiza_campo(dados['Fone'], loc.Entidade.fone)
        
    else:
        
        fone = '123456789'
        
        atualiza_campo(fone, loc.Entidade.fone)        
        
        
    btn = page.wait_for_element_to_click(loc.Entidade.bt_end)
    
    btn.click()
       
        
    if 'Cep' in dados:
        
        cep = dados['Cep']
        
        cep = cep.replace('-', '')
        
        atualiza_campo(cep, loc.Entidade.cep)
        
        cep = page.wait_for_element_to_click(loc.Entidade.bt_cep)

        cep.click()
        
        
        for i in range(30):
            
            logr = page.wait_for_element(loc.Entidade.logr)
                    
            if logr.get_attribute('value'):
                break
            
            sleep(1)
            
        else:
            
            if 'Logradouro' not in dados:
                
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], loc.Entidade.logr)
            
        if 'Número' not in dados:
            
            raise ValueError("É obrigatório informar o número na atualização\
                              do endereço")
            
        else:
            
            atualiza_campo(dados['Número'], loc.Entidade.num)
            
        if 'Complemento' in dados:
            
            atualiza_campo(dados['Complemento'], loc.Entidade.comp)
            
        bairro = page.wait_for_element(loc.Entidade.bairro)
        
        if not bairro.get_attribute('value'):
                
        
            if 'Bairro' not in dados:
                
                raise ValueError("É obrigatório informar o bairro na atualização\
                                 do endereço")
                
            else:
                
                atualiza_campo(dados['Bairro'], loc.Entidade.bairro)
                
            
    #confirmar = page.wait_for_element(loc.Entidade.confirmar)
    
    #confirmar.click()
    
    page.driver.execute_script(loc.Entidade.submit)
    
        

#driver = webdriver.Ie()
#
#ie = Page(driver)
#
#dtype_dic = {'CPF': str, 'FISTEL': str}
#
#df = pd.read_csv('files/cassacao.csv', dtype=dtype_dic)
#
#ddd = pd.read_table('files/ddd.tsv')

# retira falecidos
#df = df[df['Ano do Óbito'].isnull()]



#for i in range(58, 61):
#
#    cpf = df.iloc[i]['CPF']
#
#    if imprime_boleto(ie, cpf):
#
#        # devedores.append(name)
#        windows = ie.driver.window_handles
#
#        main = windows[0]
#
#        ie.driver.switch_to_window(windows[-1])
#
#        save_page(ie.driver, r'files/boletos/' + name + '.html')
#
#        ie.driver.close()
#
#        ie.driver.switch_to_window(main)
