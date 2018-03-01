#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""
import datetime as dt
import re
from time import sleep

import pandas as pd

import helpers
from base.page import Page

KEYS = ['processo',
        'tipo',
        'atribuicao',
        'marcador',
        'anotação',
        'prioridade',
        'peticionamento',
        'aviso',
        'situacao',
        'interessado']


def pode_expedir(linha):
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

def tag_mouseover(tag, tipo):

    tag_split = tag.attrs['onmouseover'].split("'")

    if tipo == 'anotacao':

        return ' '.join(tag_split[1:4:2])

    elif tipo == 'situacao':

        return tag_split[1]

    elif tipo == 'marcador':

        return ' '.join(tag_split[1:4:2])
    else:

        raise ValueError("O tipo de tag repassado não é válido: {}".format(tipo))

def armazena_tags(lista_tags):
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do Sei, retorna um dicionário dessas tags
    """

    dict_tags = {}

    if len(lista_tags) != 6:
        raise ValueError("Verifique o nº de tags de cada linha do \
        processo: {}. O valor diferente de 6".format(len(lista_tags)))

    dict_tags['checkbox'] = lista_tags[0].find('input', class_='infraCheckbox')

    controles = lista_tags[1].find_all('a')

    dict_tags['aviso'] = ""

    for tag_a in controles:

        img = str(tag_a.img['src'])

        if 'imagens/sei_anotacao' in img:

            dict_tags['anotacao'] = tag_mouseover(tag_a, 'anotacao')

            dict_tags['anotacao_link'] = tag_a.attrs['href']

        elif 'imagens/sei_situacao' in img:

            dict_tags['situacao'] = tag_mouseover(tag_a, 'situacao')

            dict_tags['situacao_link'] = tag_a.attrs['href']

        elif 'imagens/marcador' in img:

            dict_tags['marcador'] = tag_mouseover(tag_a, 'marcador')

            dict_tags['marcador_link'] = tag_a.attrs['href']

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

    dict_tags['link'] = processo.attrs['href']

    dict_tags['numero'] = processo.string

    dict_tags['visualizado'] = True if processo.attrs['class'] == 'processoVisualizado' else False

    tag = lista_tags[3].find('a')

    dict_tags['atribuicao'] = tag.string if tag else ''

    dict_tags['tipo'] = lista_tags[4].string


    tag = lista_tags[5].find(class_='spanItemCelula')

    dict_tags['interessado'] = tag.string if tag else ''

    return dict_tags

def tag_controle(tag):

    key, value = "", ""

    img = str(tag.img['src'])

    # TODO: change to tag.attrs.get(onmouseover)
    pattern = re.search('\((.*)\)', tag.attrs['onmouseover'])

    if 'imagens/sei_anotacao' in img:

        # Separa o texto interno retornado pelo js onmouseover delimitado
        # pelas aspas simples. Salvo somente o primeiro e terceiro items

        value = pattern.group().split("'")[1:4:2]

        key = "postit_red" if 'prioridade' in img else "postit"

    elif 'imagens/sei_situacao' in img:

        key = 'situacao'
        value = pattern.group().split("'")[1]

    elif 'imagens/marcador' in img:

        marcador = pattern.group().split("'")[1:4:2]
        key = 'marcador'
        value =  "".join(marcador)

    elif 'imagens/exclamacao' in img:

        key = 'aviso'
        value = True

    return key, value

def cria_dict_tags(lista_tags):
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do SEI, retorna um dicionário dessas tags
    """

    dict_tags = {key:"" for key in keys}

    assert len(lista_tags) == 6, "Verifique o nº de tags de cada linha do \
    processo, valor diferente de 10"

    controles = {k:v for k, v in tag_controle(tag) for tag in lista_tags[1].find_all('a')}

    dict_tags = {**dict_tags, **controles}

    peticionamento = lista_tags[1].find(src=re.compile('peticionamento'))

    if peticionamento:

        pattern = re.search(
            '\((.*)\)', peticionamento.attrs['onmouseover'])

        dict_tags['peticionamento'] = pattern.group().split('"')[1]

    processo = lista_tags[2].find('a')

    dict_tags['processo'] = processo.string

    atribuicao =  lista_tags[3].find("a")

    if atribuicao:

        dict_tags['atribuicao'] = atribuicao.string

    dict_tags['tipo'] = lista_tags[4].string


    interessado = lista_tags[5].find(class_='spanItemCelula')

    if interessado:

        dict_tags['interessado'] = interessado.string

    return dict_tags

def dict_to_df(processos):
    """Recebe a lista processos contendo um dicionário das tags de cada
    processo aberto no SEI. Retorna um Data Frame cujos registros
    são as string das tags.
    """

    cols = ['processo', 'tipo', 'atribuicao', 'marcador', 'anotacao', 'prioridade',
            'peticionamento', 'aviso', 'situacao', 'interessado']

    df = pd.DataFrame(columns=cols)

    for p in processos:
        df = df.append(pd.Series(p), ignore_index=True)

    df['atribuicao'] = df['atribuicao'].astype("category")
    df['prioridade'] = df['prioridade'].astype("category")
    df['tipo'] = df['tipo'].astype("category")

    return df

def init_browser(webdriver, login, senha):

    page = Page(webdriver)

    page.driver.get('http://sistemasnet')

    sleep(1)

    alert = page.alert_is_present(timeout=10)


    if alert:

        try:

            alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

            alert.accept()

        except:

            return page

    return page

def check_input(ident, serv, tipo):

    if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:

        raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

    if tipo == 'cnpj' and len(ident) != 14:

        raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

    ident = str(ident)

    tipo = str(tipo)

    if serv == "cidadao":

        pattern = r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$'

        sis = sei.helpers.Scpx

    elif serv == 'radioamador':

        pattern = r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$'

        sis = Scra

    elif serv == "aeronautico":

        pattern = r'^(P){1}([A-Z]){4}$'

        sis = Slma

    elif serv == "maritimo":

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

    return (ident, tipo, sis)

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