# -*- coding: utf-8 -*-
#!usr/bin/env python3
"""
Created on Tue Nov  7 14:05:59 2017

@author: rsilva
"""

import datetime as dt
import os
import re
from time import sleep

from locators import Boleto, Sec, Entidade, Scpx, Scra, Slmm, Slma, Sigec
from selenium.webdriver.common.keys import Keys

from page import Page

os.chdir(r'C:\Users\rsilva\Google Drive\projects\programming\automation')


def init_browser(webdriver, login, senha):

    page = Page(webdriver)

    page.driver.get('http://sistemasnet')

    # sleep(1)

    alert = page.alert_is_present(timeout=5)


    if alert:

        try:

            alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

            alert.accept()

        except:

            return page

    return page


def save_page(page, filename):

    with open(filename, 'w') as file:

        #html = soup(driver.page_source).prettify()

        # write image
        file.write(page.driver.page_source)

        # TODO: install weasyprint

        # TODO; autoit

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
    page.driver.get(Boleto.URL)

    if id_type in ('cpf', 'cnpj'):

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

    except:

        print("Não foi possível marcar todos os boletos")

        return False

    try:

        imprimir = page.wait_for_element_to_click(Boleto.PRINT)

        imprimir.click()

    except:

        print("Não foi possível imprimir todos os boletos")

    #     return False
    #
    # try:
    #
    #     page.wait_for_new_window()
    #
    # except:
    #
    #     print("A espera pela nova janela não funcionou!")
    #
    #     return False
    #
    # try:
    #
    #     windows = page.driver.window_handles
    #
    #     main = windows[0]
    #
    #     boleto = windows[1]
    #
    #     page.driver.switch_to_window(boleto)
    #
    #     save_page(page, ident)
    #
    #
    #
    #     page.close()
    #
    #     page.driver.switch_to_window(main)
    #
    # except:
    #
    #     print("Não foi possível salvar a nova janela")
    #
    #
    #
    #     return False
    #
    # return True


def atualiza_cadastro(page, dados):
    
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
    page.driver.get(Sec.Ent_Alt)
    
    cpf = page.wait_for_element_to_click(Entidade.cpf)
    
    cpf.send_keys(str(dados['CPF']) + Keys.RETURN)
       
        
    if 'Email' in dados:
        
        atualiza_campo(dados['Email'], Entidade.email)
        
    btn = page.wait_for_element_to_click(Entidade.bt_dados)
    
    btn.click()
            
    if 'RG' in dados:
        
        atualiza_campo(dados['RG'], Entidade.rg)
        
    if 'Orgexp' in dados:
        
        atualiza_campo(dados['Orgexp'], Entidade.orgexp)
        
    if 'Data de Nascimento' in dados:
        
        data = dados['Data de Nascimento']
        
        data = data.replace('-', '')
        
        atualiza_campo(data, Entidade.nasc)
        
    btn = page.wait_for_element_to_click(Entidade.bt_fone)
    
    btn.click()
    
        
    if 'ddd' in dados:
        
        atualiza_campo(dados['ddd'], Entidade.ddd)
        
    else:
        
        ddd = '11'
        
        atualiza_campo(ddd, Entidade.ddd)

        
    #if 'Fone' in dados:
        
     #   atualiza_campo(dados['Fone'], Entidade.fone)
        
    #else:
        
     #   fone = '123456789'
        
      #  atualiza_campo(fone, Entidade.fone)
        
        
    btn = page.wait_for_element_to_click(Entidade.bt_end)
    
    btn.click()
       
        
    if 'Cep' in dados:
        
        cep = dados['Cep']
        
        cep = cep.replace('-', '')
        
        atualiza_campo(cep, Entidade.cep)
        
        cep = page.wait_for_element_to_click(Entidade.bt_cep)

        cep.click()
        
        
        for i in range(30):
            
            logr = page.wait_for_element(Entidade.logr)
                    
            if logr.get_attribute('value'):
                break
            
            sleep(1)
            
        else:
            
            if 'Logradouro' not in dados:
                
                raise ValueError("É Obrigatório informar o logradouro")
            atualiza_campo(dados['Logradouro'], Entidade.logr)
            
        if 'Número' not in dados:
            
            raise ValueError("É obrigatório informar o número na atualização\
                              do endereço")
            
        else:
            
            atualiza_campo(dados['Número'], Entidade.num)
            
        if 'Complemento' in dados:
            
            atualiza_campo(dados['Complemento'], Entidade.comp)
            
        bairro = page.wait_for_element(Entidade.bairro)
        
        if not bairro.get_attribute('value'):
                
        
            if 'Bairro' not in dados:
                
                raise ValueError("É obrigatório informar o bairro na atualização\
                                 do endereço")
                
            else:
                
                atualiza_campo(dados['Bairro'], Entidade.bairro)
                
            
    #confirmar = page.wait_for_element(Entidade.confirmar)
    
    #confirmar.click()
    
    page.driver.execute_script(Entidade.submit)
    
def check_input(ident, serv, tipo):

    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:

        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:

        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

    ident = str(ident).upper()

    serv = str(serv)

    tipo = str(tipo)

    if serv == "400":

        pattern = r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$'

        sis = Scpx

    elif serv == '302':

        pattern = r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$'

        sis = Scra

    elif serv == "507":

        pattern = r'^(P){1}([A-Z]){4}$'

        sis = Slma

    elif serv == "604":

        pattern = r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})'

        sis = Slmm

    elif serv == "boleto":

        sis = Boleto

    elif serv == "sec":

        sis = Sec

    else:

        raise ValueError("Não foi encontrado o Serviço {}".format(serv))

    if tipo == 'indicativo':

        if not re.match(pattern, ident, re.I):

            raise ValueError("Indicativo Digitado Inválido")

    return (ident, serv, tipo, sis)

def navigate(page, ident, tipo):

    for id in Entidade[tipo]:

        try:

            elem = page.wait_for_element_to_click(id, timeout=3)

            elem.send_keys(ident + Keys.RETURN)

            break

        except:

            next

    else:

        print("Não foi encontrado o 'id' do identificador {} na página".format(tipo))



def consulta(page, ident, serv, tipo):

    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Consulta)

    navigate(page, ident, tipo)


def incluir_estacao(page, ident, serv, tipo):

    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Estacao['incluir'])

    navigate(page, ident, tipo)


def imprime_licenca(page, ident, serv, tipo):

    ident, serv, tipo, sis = check_input(ident, serv, tipo)

    page.driver.get(sis.Licenca['Imprimir'])

    navigate(page, ident, sis.Licenca, tipo)


def consultaSigec(page, ident, tipo='cpf'):


    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:

        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:

        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))


    page.driver.get(Sigec.consulta)

    if tipo in ('cpf', 'cnpj'):

        elem = page.wait_for_element_to_click(Sigec.cpf)

        elem.send_keys(ident + Keys.RETURN)

    elif tipo == 'fistel':

        elem = page.wait_for_element_to_click(Sigec.fistel)

        elem.send_keys(ident + Keys.RETURN)

    page.wait_for_page_load()


    # TODO: implement other elements

