#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""
import re

import pandas as pd


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

    dict_tags['aviso'] = ''

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

    try:

        dict_tags['atribuicao'] = lista_tags[3].find('a').string

    except:

        dict_tags['atribuicao'] = ''

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
