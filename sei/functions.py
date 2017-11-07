# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""

import re

import os

os.chdir('../')

# Selenium Methods
from selenium.webdriver.common.keys import Keys

from locators import Base




def podeExpedir(p):

    t1 = p['processo'].find_all('a', class_="protocoloAberto")

    t2 = p['tipo'].find_all(string="Ofício")

    t3 = p['assinatura'].find_all(string=re.compile("Coordenador"))

    t4 = p['assinatura'].find_all(string=re.compile("Gerente"))

    return bool(t1) and bool(t2) and (bool(t3) or bool(t4))


def navigate_elem_to_new_window(driver, elem):
    """ Receive an instance of Page, navigate the link to a new window

        focus the driver in the new window

        return the main window and the driver focused on new window

        Assumes link is in page
    """
    # Guarda janela principal
    main_window = driver.current_window_handle

    # Abre link no elem em uma nova janela
    elem.send_keys(Keys.SHIFT + Keys.RETURN)

    # Guarda as janelas do navegador presentes
    windows = driver.window_handles

    # Troca o foco do navegador
    driver.switch_to_window(windows[-1])

    return (main_window, windows[-1])


def navigate_link_to_new_window(driver, link):

    # Guarda janela principal
    main_window = driver.current_window_handle

    # Abre link no elem em uma nova janela
    # body = self.driver.find_element_by_tag_name('body')

    # body.send_keys(Keys.CONTROL + 'n')

    driver.execute_script("window.open()")
    # Guarda as janelas do navegador presentes
    windows = driver.window_handles

    # Troca o foco do navegador
    driver.switch_to_window(windows[-1])

    driver.get(link)

    return (main_window, windows[-1])


def cria_dict_tags(lista_tags):

    dict_tags = {}
    
    assert len(lista_tags) == 6, "Verifique o nº de tags de cada linha do processo, valor diferente de 10"

    #dict_tags['checkbox'] = lista_tags[0].find(class_='infraCheckbox')
    
    controles = lista_tags[1].find_all('a')
    
    dict_tags['AVISO'] = 'NÃO'
    
    for tag_a in controles:
        
        img = str(tag_a.img['src'])       
        
        
        if 'imagens/sei_anotacao' in img:
            
            #dict_tags['ANOTACAO'] = tag_a
            
            dict_tags['ANOTACAO'] = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group().split("'")[1:4:2]
            
            if 'PRIORIDADE' in img: 
                
                dict_tags['PRIORIDADE'] = 'SIM'
                
            else:                
                
                dict_tags['PRIORIDADE'] = 'NÃO'
            
        elif 'imagens/sei_situacao' in  img:
            
            dict_tags['SITUACAO'] = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group().split("'")[1]
            
        elif 'imagens/marcador' in img:
            
            #dict_tags['MARCADOR'] = tag_a
            
            marcador = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group().split("'")[1:4:2]
            
            dict_tags['MARCADOR'] = marcador[1]
            
            dict_tags['TEXTO-MARCADOR'] = marcador[0]
            
            
        elif 'imagens/exclamacao' in img:                        
           
            #dict_tags['AVISO'] = re.search('(\(\')(.*)(\'\))', tag_a.attrs['onmouseover']).group(2)
            
            dict_tags['AVISO'] = 'SIM'
            
            
            
        peticionamento = lista_tags[1].find(src = re.compile('peticionamento'))
        
        if peticionamento:
            
            dict_tags['PETICIONAMENTO'] = re.search('\((.*)\)', peticionamento.attrs['onmouseover']).group().split('"')[1]
            
            
    processo = lista_tags[2].find('a')
    
    dict_tags['PROCESSO'] = processo.string    
    
    #dict_tags['VISUALIZADO'] = processo.attrs['class'][0]
    
    #dict_tags['link'] = Base.NAV_URL + processo.attrs['href']
    
    
    try:
        dict_tags['ATRIBUICAO'] = lista_tags[3].find('a').string
    
    except:        
        
        pass
                
    dict_tags['TIPO'] = lista_tags[4].string
    
    try:
        dict_tags['INTERESSADO'] = lista_tags[5].find(class_='spanItemCelula').string
        
    except: 
        
        pass
        
        
    return dict_tags     

def dict_to_df(processos):

    tags = ['PROCESSO','TIPO', 'ATRIBUICAO', 'MARCADOR', 'TEXTO-MARCADOR', 'ANOTACAO', 'PRIORIDADE',
            'PETICIONAMENTO', 'AVISO', 'SITUACAO','INTERESSADO']

    df = pd.DataFrame(columns=tags)

    for p in processos:

        df = df.append(pd.Series(p), ignore_index=True)
        
    #df['VISUALIZADO'] = df['VISUALIZADO'].astype("category")
    df['ATRIBUICAO'] = df['ATRIBUICAO'].astype("category")
    df['PRIORIDADE'] = df['PRIORIDADE'].astype("category")
    df['TIPO'] = df['TIPO'].astype("category")
    
    #df['VISUALIZADO'].cat.categories = ['NÃO', 'SIM']
    
    
    return df    

