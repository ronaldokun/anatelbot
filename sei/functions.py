# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""

import re

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

def lista_to_dict_tags(lista_tags):

    dict_tags = {}
    
    assert len(lista_tags) == 6, \
    "Verifique o nº de tags de cada linha do processo, valor diferente de 10"

    dict_tags['checkbox'] = lista_tags[0].find(class_='infraCheckbox')
    
    # Existem no máximo 4 tags 'a' nos controles dos processos como
    # tags filhas da 2ª tag
    controles = lista_tags[1].find_all('a')    
    
    # itera e classifica as tags filhas
    for tag_a in controles:
        
        img = str(tag_a.img['src'])
        
        # por default as anotações não estão como prioridade ( vermelhas )        
        dict_tags['prioridade'] = False
        
        # testa se a tag ép Post-It
        if 'imagens/sei_anotacao' in img:
                        
            txt = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group()
            
            txt = txt.split("'")[1:4:2]
            
            dict_tags['post-it'] = txt
            
            dict_tags['link_post-it'] =  Base.NAV_URL + tag_a['href']
            
            if 'prioridade' in img: 
                
                dict_tags['prioridade'] = True
        # testa se é Ponto de Controle
        elif 'imagens/sei_situacao' in  img:
            
            txt = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group()
            
            txt = txt.split("'")[1]
            
            dict_tags['situacao'] = txt
            
            dict_tags['link_situacao'] = Base.NAV_URL + tag_a['href']
        
        # testa se a tag é um marcador
        elif 'imagens/marcador' in img:
            
            dict_tags['link_marcador'] = Base.NAV_URL + tag_a['href']
            
            txt = re.search('\((.*)\)', tag_a.attrs['onmouseover']).group()
            
            txt = txt.split("'")[1:4:2]
            
            dict_tags['marcador'] = txt[1] + ' : ' + txt[0]            
            
        # testa se a tag é um aviso   
        elif 'imagens/exclamacao' in img: 

            txt = re.search('(\(\')(.*)(\'\))', tag_a.attrs['onmouseover']).group(2)                     
           
            dict_tags['aviso'] = txt
            
        # o peticionamento não aparece como tag 'a' mas sim como tag 'img'   
        pet = lista_tags[1].find(src = re.compile('peticionamento'))
        
        if pet:
            
            txt = re.search('\((.*)\)', pet.attrs['onmouseover']).group()
            
            txt = txt.split('"')[1]
            
            dict_tags['peticionamento'] = txt
            
            
    processo = lista_tags[2].find('a')
    
    if processo['class'] == 'processoNaoVisualizado':
        
        dict_tags['visualizado'] = 'NÃO'
        
    else: dict_tags['visualizado'] = 'SIM'
    
    dict_tags['link_processo'] = Base.NAV_URL + processo['href']
    
    txt = re.search("(\)(.*)(\))", processo['onmouseover']).group(2)
    
    dict_tags['detalhes'] = txt.split(',')[0]
    
    
    try:
        dict_tags['atribuicao'] = lista_tags[3].find('a').string
    
    except:        
        
        dict_tags['atribuicao'] = ''
        
                
    dict_tags['tipo'] = lista_tags[4].string
    
    try:
        dict_tags['interessado'] = lista_tags[5].find(class_='spanItemCelula').string
        
    except: 
        
        dict_tags['interessado'] = ''
        
        
    return {processo.string:dict_tags}    

