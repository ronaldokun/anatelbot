#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""
# Basic Bultins
import datetime as dt
import re
import itertools

import pandas as pd


from selenium.webdriver.common.keys import Keys

from page import Page

URL = "https://sei.anatel.gov.br/sei/"

KEYS = [
    "processo",
    "tipo",
    "atribuicao",
    "marcador",
    "anotação",
    "prioridade",
    "peticionamento",
    "aviso",
    "situacao",
    "interessado",
]

PADRAO_IND = [
    r"^(P){1}(X){1}(\d){1}([A-Z]){1}(\d){4}$",
    r"^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$",
    r"^(P){1}([A-Z]){4}$",
    r"^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})",
]

STRIP = ("/", ".", "-")


def strip_string(identificador: str, strip: tuple = STRIP) -> str:
    """Remove os caracteres contidos em strip do identificador
    
    Args:
        identificador (str): String a ser processada
        strip (tuple, optional): Tupla com caracteres a serem removidos. Defaults to STRIP.
    
    Returns:
        str: String `identificador` formatada.
    """
    return "".join(s for s in identificador if s not in strip)


def init_browser(webdriver, login, senha, timeout=10):

    page = Page(webdriver)

    page.driver.get("http://sistemasnet")

    alert = page.alert_is_present(timeout=timeout)

    if alert:

        # page.driver.switch_to.alert()

        alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

        alert.accept()

    return page


def check_input(identificador: str, tipo: str) -> str:
    """Checa se o identificador do tipo informado é válido

    Raises:
        ValueError: ValueError caso o nº de caracteres informado exceda o padrão para cpf, fistel e cnpj
        ValueError: Caso o indicativo consultado não siga o padrão da legislação


    Returns:
        str: identificador opcionalmente adicionado zeros caso seja menor que o tamanho padrão.
    """

    identificador = strip_string(str(identificador))

    size = 11

    if tipo == "indicativo":

        for pattern in PADRAO_IND:

            if re.match(pattern, identificador, re.I):
                return identificador
        else:

            raise ValueError(
                f"O identificador {identificador} do tipo {tipo} é inválido"
            )

    elif tipo == "cpf" or tipo == "fistel":
        if len(identificador) > size:
            raise ValueError(
                f"O identificador {identificador} do tipo {tipo} deve ter 11 dígitos"
            )

    elif tipo == "cnpj":
        size = 14
        if len(identificador) > size:
            raise ValueError(
                f"O identificador {identificador} do {tipo} deve ter 14 dígitos"
            )

    while len(identificador) < size:
        identificador += "0" + identificador

    return identificador


def last_day_of_month():
    """ Use datetime module and manipulation to return the last day
        of the current month, it's doesn't matter which.
        Return: Last day of current month, valid for any month
    """
    any_day = dt.date.today()

    next_month = any_day.replace(day=28) + dt.timedelta(days=4)  # this will never fail

    # this will always result in the last day of the month
    date = next_month - dt.timedelta(days=next_month.day)

    date = date.strftime("%d%m%y")

    return date


def transform_date(date):

    try:
        formated = dt.datetime.strptime(str(date), "%d/%m/%Y").date()

    except:

        formated = dt.datetime.strptime(str(date), "%Y-%m-%d").date()

    return formated


def lastRow(ws, col=2):
    """ Find the last row in the worksheet that contains data.

    idx: Specifies the worksheet to select. Starts counting from zero.

    workbook: Specifies the workbook

    col: The column in which to look for the last cell containing data.
    """

    # ws = workbook.sheets[idx]

    lwr_r_cell = ws.cells.last_cell  # lower right cell
    lwr_row = lwr_r_cell.row  # row of the lower right cell
    lwr_cell = ws.range((lwr_row, col))  # change to your specified column

    if lwr_cell.value is None:
        lwr_cell = lwr_cell.end("up")  # go up untill you hit a non-empty cell

    return lwr_cell.row


def extrai_pares_tabulação(source):
    trs = source.find_all("tr")
    dados = {}
    i = 1
    for tr in trs:
        td = tr.find_all("td", string=True)
        label = tr.find_all("label", string=True)

        i = 1
        for field, result in zip(td, label):
            field, result = field.text[:-1], result.text
            if field in dados:
                field = field + "_" + str(i + 1)
            dados[field] = result

    return dados


def add_point_cpf_cnpj(ident):

    ident = strip_string(ident)

    while len(ident) < 11:
        ident += "0" + ident

    if len(ident) == 11:
        return f"{ident[:3]}.{ident[3:6]}.{ident[6:9]}-{ident[9:]}"

    if len(ident) == 14:
        return f"{ident[:2]}.{ident[2:5]}.{ident[5:8]}/{ident[8:12]}-{ident[12:]}"

