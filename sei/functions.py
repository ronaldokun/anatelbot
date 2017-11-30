#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""

from sei import re, pd, soup, Keys, By

from sei import locators as loc
from sei.pages import Sei

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


def nav_elem_to_new_win(driver, elem):
    """ navigate the link present in element to a new window
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


def nav_link_to_new_win(driver, link):

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

def armazena_tags(lista_tags):
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do Sei, retorna um dicionário dessas tags
    """
    
    dict_tags = {}
    
    assert len(lista_tags) == 6, "Verifique o nº de tags de cada linha do \
    processo, valor diferente de 10"
    
    dict_tags['checkbox'] = lista_tags[0].find('input', class_ = 'infraCheckbox')

    controles = lista_tags[1].find_all('a')

    dict_tags['aviso'] = False

    for tag_a in controles:

        img = str(tag_a.img['src'])

        if 'imagens/sei_anotacao' in img:

            dict_tags['anotacao'] = tag_a

        elif 'imagens/sei_situacao' in img:

            dict_tags['situacao'] = tag_a

        elif 'imagens/marcador' in img:

            dict_tags['marcador'] = tag_a

        elif 'imagens/exclamacao' in img:

            dict_tags['aviso'] = True

        peticionamento = lista_tags[1].find(src=re.compile('peticionamento'))

        if peticionamento:

            pattern = re.search(
                '\((.*)\)', peticionamento.attrs['onmouseover'])
            dict_tags['peticionamento'] = pattern.group().split('"')[1]
            
        else:
            
            dict_tags['peticionamento'] = ''

    processo = lista_tags[2].find('a')

    dict_tags['processo'] = processo

    try:

        dict_tags['atribuicao'] = lista_tags[3].find('a')

    except:

        pass

    dict_tags['tipo'] = lista_tags[4].string

    try:
        
        dict_tags['interessado'] = lista_tags[5].find(
            class_='spanItemCelula').string

    except:

        dict_tags['interessado'] = ''

    return dict_tags
    


def cria_dict_tags(lista_tags):
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do SEI, retorna um dicionário dessas tags
    """

    dict_tags = {}

    assert len(lista_tags) == 6, "Verifique o nº de tags de cada linha do \
    processo, valor diferente de 10"

    controles = lista_tags[1].find_all('a')

    dict_tags['aviso'] = 'NÃO'

    for tag_a in controles:

        img = str(tag_a.img['src'])

        pattern = re.search('\((.*)\)', tag_a.attrs['onmouseover'])

        if 'imagens/sei_anotacao' in img:

            # Separa o texto interno retornado pelo js onmouseover delimitado
            # pelas aspas simples. Salvo somente o primeiro e terceiro items
            dict_tags['ANOTACAO'] = pattern.group().split("'")[1:4:2]

            if 'prioridade' in img:

                dict_tags['prioridade'] = 'SIM'

            else:

                dict_tags['prioridade'] = 'NÃO'

        elif 'imagens/sei_situacao' in img:

            dict_tags['situacao'] = pattern.group().split("'")[1]

        elif 'imagens/marcador' in img:

            marcador = pattern.group().split("'")[1:4:2]

            dict_tags['marcador'] = marcador[1]

            dict_tags['TEXTO-MARCADOR'] = marcador[0]

        elif 'imagens/exclamacao' in img:

            dict_tags['aviso'] = 'SIM'

        peticionamento = lista_tags[1].find(src=re.compile('peticionamento'))

        if peticionamento:

            pattern = re.search(
                '\((.*)\)', peticionamento.attrs['onmouseover'])
            dict_tags['peticionamento'] = pattern.group().split('"')[1]

    processo = lista_tags[2].find('a')

    dict_tags['processo'] = processo.string

    try:

        dict_tags['atribuicao'] = lista_tags[3].find('a').string

    except:

        pass

    dict_tags['tipo'] = lista_tags[4].string

    try:
        dict_tags['interessado'] = lista_tags[5].find(
            class_='spanItemCelula').string

    except:

        pass

    return dict_tags


def string_of_tags(tags):
    
    func = lambda x: x.attrs['onmouseover'].split("'")
    
    if 'anotacao' in tags:
        
        tags['anotacao'] = ' '.join(func(tags['anotacao'])[1:4:2])
        
    if 'situacao' in tags:
        
        tags['situacao'] = func(tags['situacao'])[1]
        
    if 'marcador' in tags:
        
        tags['marcador'] = ' '.join(func(tags['marcador'])[1:4:2])
        
    return tags

def dict_to_df(processos):
    """Recebe a lista processos contendo um dicionário das tags de cada
    processo aberto no SEI. Retorna um Data Frame cujos registros
    são as string das tags.
    """
    
    cols = ['processo', 'tipo', 'atribuicao', 'marcador', 'anotacao','prioridade',
            'peticionamento', 'aviso', 'situacao', 'interessado']

    df = pd.DataFrame(columns=cols)
    
    for p in processos:
        
        df = df.append(pd.Series(string_of_tags(p)), ignore_index=True)
    
    df['atribuicao'] = df['atribuicao'].astype("category")
    df['prioridade'] = df['prioridade'].astype("category")
    df['tipo'] = df['tipo'].astype("category")

    return df


def ir_pagina_contato(page):

    if not isinstance(page, Sei):
        raise TypeError("Object {0} must be of instance {1}".format(page, Sei))

    html = soup(page.driver.page_source, 'lxml')

    tag = html.find('li', string='Listar')

    if not tag:
        raise LookupError("The tag of type {0} and string {1} is not present in the page".format('<li>', 'Listar'))

    link = tag.a.attrs['href']

    page.go(link)

def consulta_contato(page, nome):

    if page.get_title() != 'Sei - Contatos':
        ir_pagina_contato(page)

    contato = page.wait_for_element_to_click(loc.Tipos.CONTATO)

    contato.clear()

    contato.send_keys(nome + Keys.RETURN)

    if not page.elem_is_visible(By.LINK_TEXT, "Nenhum Registro Encontrado"):

        page.wait_for_element_to_be_visible(By.CLASS_NAME, 'infraTrClara')

        html = soup(page.driver.page_source, 'lxml')

        tags = html.find_all('tr', class_='infraTrClara')

        return (len(tags), tags)

    return (0,'')









def cadastrar_interessado(Sei, nome, dados, tipo='pf', ):

    pass


def cria_processo(Sei, tipo, desc='', inter='', nivel='público'):

    tipo = str(tipo)

    assert tipo in loc.Tipos.PROCS,\
        print("O tipo de processo digitado {0}, não é válido".format(str(tipo)))

    
    Sei.exibir_menu_lateral()
    
    init_proc = Sei.wait_for_element_to_click(loc.LatMenu.INIT_PROC)
    
    init_proc.click()
    
    filtro = Sei.wait_for_element_to_click(loc.Tipos.FILTRO)
    
    filtro.send_keys(tipo)
    
    # exibe_todos = Sei.wait_for_element_to_click(loc.Tipos.EXIBE_ALL)
    
    # exibe_todos.click()


    # select = Select(Sei.wait_for_element(loc.Tipos.SL_TIP_PROC))

    tipo = Sei.wait_for_element_to_click((By.LINK_TEXT, tipo))
    
    tipo.click()

    if desc:

        espec = Sei.wait_for_element(loc.Processo.ESPEC)

        espec.send_keys(desc)

    if inter:

        Sei.cadastrar_interessado(inter)
        Sei.consultar_contato(inter)

    if nivel == 'público':

        nivel = Sei.wait_for_element(loc.Processo.PUBL)

    elif nivel == 'restrito':

        nivel = Sei.wait_for_element(loc.Processo.REST)

    else:

        nivel = Sei.wait_for_element(loc.Processo.SIG)

    nivel.click()
    

def exibir_bloco(Sei, numero):

    if Sei.get_title() != loc.Blocos.TITLE:
        Sei.go_to_blocos()

    try:
        Sei.wait_for_element((By.LINK_TEXT, str(numero))).click()

    except:
        print("O Bloco de Assinatura informado não existe ou está \
              concluído!")

def armazena_bloco(Sei, numero):

    if Sei.get_title() != loc.Bloco.TITLE + " " + str(numero):

        Sei.exibir_bloco(numero)

    html_bloco = soup(Sei.driver.page_source, "lxml")
    linhas = html_bloco.find_all(
        "tr", class_=['infraTrClara', 'infraTrEscura'])

    chaves = ['checkbox', 'seq', "processo", 'documento', 'data', 'tipo',
              'assinatura', 'anotacoes', 'acoes']

    lista_processos = []

    for linha in linhas:

        proc = {k: None for k in chaves}

        cols = [v for v in linha.contents if v != "\n"]

        assert len(chaves) == len(cols), "Verifique as linhas do bloco!"

        for k, v in zip(chaves, cols):

            proc[k] = v

        # proc["expedido"] = False

        lista_processos.append(proc)

    return lista_processos

def expedir_bloco(Sei, numero):

    processos = Sei.armazena_bloco(numero)

    for p in processos:
       
        if ft.podeExpedir(p):

            proc = p['processo'].a.string

            num_doc = p['documento'].a.string

            link = loc.Base.URL + p['processo'].a.attrs['href']

            (bloco_window, proc_window) = ft.nav_link_to_new_win(
                Sei.driver, link)

            processo = Processo(Sei.driver, proc_window)

            processo.expedir_oficio(proc, num_doc, link)



