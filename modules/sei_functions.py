#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""

import re

import pandas as pd

import datetime as dt


# Selenium Methods
from selenium.webdriver.common.keys import Keys

from modules.locators import Boleto


def podeExpedir(linha):
    """Verifica algumas condições necessárias para expedição do Ofício no SEI
    Args:
        linha: Dicionário das html tags presentes nas linhas
                   do bloco de assinatura.

        Return: Boolean
    """

    t1 = linha['processo'].find_all('a', class_="protocoloAberto")

    t2 = linha['tipo'].find_all(string="Ofício")

    t3 = linha['assinatura'].find_all(string=re.compile("Coordenador"))

    t4 = linha['assinatura'].find_all(string=re.compile("Gerente"))

    return bool(t1) and bool(t2) and (bool(t3) or bool(t4))


def navigate_elem_to_new_window(driver, elem):
    """ Navigate the link present in element to a new window
        focus the page on the new window
        Assumes the is a link present in the html element 'elem' 
        Args:
           driver: Selenium webdriver object 
           elem: html element with navigable link
        Return:
            tuple with both webdriver windows objects
            with the browser focused on the new one. 
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
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do SEI, retorna um dicionário dessas tags
    """

    dict_tags = {}

    assert len(lista_tags) == 6, "Verifique o nº de tags de cada linha do \
    processo, valor diferente de 10"

    controles = lista_tags[1].find_all('a')

    dict_tags['AVISO'] = 'NÃO'

    for tag_a in controles:

        img = str(tag_a.img['src'])

        pattern = re.search('\((.*)\)', tag_a.attrs['onmouseover'])

        if 'imagens/sei_anotacao' in img:

            # Separa o texto interno retornado pelo js onmouseover delimitado
            # pelas aspas simples. Salvo somente o primeiro e terceiro items
            dict_tags['ANOTACAO'] = pattern.group().split("'")[1:4:2]

            if 'PRIORIDADE' in img:

                dict_tags['PRIORIDADE'] = 'SIM'

            else:

                dict_tags['PRIORIDADE'] = 'NÃO'

        elif 'imagens/sei_situacao' in img:

            dict_tags['SITUACAO'] = pattern.group().split("'")[1]

        elif 'imagens/marcador' in img:

            marcador = pattern.group.split("'")[1:4:2]

            dict_tags['MARCADOR'] = marcador[1]

            dict_tags['TEXTO-MARCADOR'] = marcador[0]

        elif 'imagens/exclamacao' in img:

            dict_tags['AVISO'] = 'SIM'

        peticionamento = lista_tags[1].find(src=re.compile('peticionamento'))

        if peticionamento:

            pattern = re.search(
                '\((.*)\)', peticionamento.attrs['onmouseover'])
            dict_tags['PETICIONAMENTO'] = pattern.group().split('"')[1]

    processo = lista_tags[2].find('a')

    dict_tags['PROCESSO'] = processo.string

    try:

        dict_tags['ATRIBUICAO'] = lista_tags[3].find('a').string

    except:

        pass

    dict_tags['TIPO'] = lista_tags[4].string

    try:
        dict_tags['INTERESSADO'] = lista_tags[5].find(
            class_='spanItemCelula').string

    except:

        pass

    return dict_tags


def dict_to_df(processos):
    """Recebe a lista processos contendo um dicionário das tags de cada
    linha de processo aberto no SEI. Retorna um Data Frame cujos registros
    são cada linha de processos.
    """

    tags = ['PROCESSO', 'TIPO', 'ATRIBUICAO', 'MARCADOR', 'TEXTO-MARCADOR',
            'ANOTACAO', 'PRIORIDADE', 'PETICIONAMENTO', 'AVISO', 'SITUACAO',
            'INTERESSADO']

    df = pd.DataFrame(columns=tags)

    for p in processos:

        df = df.append(pd.Series(p), ignore_index=True)

    df['ATRIBUICAO'] = df['ATRIBUICAO'].astype("category")
    df['PRIORIDADE'] = df['PRIORIDADE'].astype("category")
    df['TIPO'] = df['TIPO'].astype("category")

    return df


