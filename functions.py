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

# Google Spreadsheet and DataFrame tools
import gspread
import gspread_dataframe as gs_to_df
import pandas as pd

# Authentication @Google
from oauth2client.service_account import ServiceAccountCredentials


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


def pode_expedir(linha: dict) -> bool:
    """Verifica se a linha do Bloco de Assinatura do Sei está assinada
    
    Args:
        linha (dict): Dicionário com as informações da Linha do Bloco: Processo, tipo, assinatura, 
    
    Returns:
        bool
        True, 
            * Se o Processo está Aberto,
            * Se Tipo = Ofício
            * Contém assinatura Coordenador/Gerente
        False,
        Se um dos casos acima falhar
    """

    t1 = linha["processo"].find_all("a", class_="protocoloAberto")

    t2 = linha["tipo"].find_all(string="Ofício")

    t3 = linha["assinatura"].find_all(string=re.compile("Coordenador"))

    t4 = linha["assinatura"].find_all(string=re.compile("Gerente"))

    return bool(t1) and bool(t2) and (bool(t3) or bool(t4))


def tag_mouseover(tag, tipo: str):
    # TODO: Document with bs4 type

    tag_split = tag.attrs["onmouseover"].split("'")

    if tipo in ("anotacao", "marcador"):

        return " ".join(tag_split[1:4:2])

    elif tipo == "situacao":

        return tag_split[1]

    else:

        raise ValueError("O tipo de tag repassado não é válido: {}".format(tipo))


def cria_dict_acoes(acoes: list) -> dict:

    """Recebe uma lista de html tags 'a' e retorna um dicionário dessas tags
    
    Args:
        acoes (list): HTML 'a' tags
    
    Returns:
        dict: Dicionário - key=tag title, value=tag link or Javascript function string
    """
    dict_tags = {}

    for tag in acoes:

        key = tag.contents[0].attrs["title"]

        if tag.attrs["href"] != "#":

            dict_tags[key] = URL + tag.attrs["href"]

        else:

            dict_tags[key] = str(tag.attrs["onclick"])

    return dict_tags


def armazena_tags(lista_tags: list) -> dict:
    """Recebe uma lista de tags de cada linha do processo  da página inicial
    do Sei, retorna um dicionário dessas tags
    
    Args:
        lista_tags (list): Lista de Tags contida na tag tabular definida por 
        cada linha de processo da página inicial do SEI
    
    Returns:
        dict: dicionário - key=Nome da Tag, value=string ou objeto tag
    """

    assert (
        len(lista_tags) == 6
    ), "Verifique o nº de tags de cada linha do \
        processo: {}. O valor diferente de 6".format(
        len(lista_tags)
    )

    dict_tags = {}

    dict_tags["checkbox"] = lista_tags[0].find("input", class_="infraCheckbox")

    controles = lista_tags[1].find_all("a")

    dict_tags["aviso"] = ""

    for tag_a in controles:

        img = str(tag_a.img["src"])

        if "imagens/sei_anotacao" in img:

            dict_tags["anotacao"] = tag_mouseover(tag_a, "anotacao")

            dict_tags["anotacao_link"] = URL + tag_a.attrs["href"]

        elif "imagens/sei_situacao" in img:

            dict_tags["situacao"] = tag_mouseover(tag_a, "situacao")

            dict_tags["situacao_link"] = URL + tag_a.attrs["href"]

        elif "imagens/marcador" in img:

            dict_tags["marcador"] = tag_mouseover(tag_a, "marcador")

            dict_tags["marcador_link"] = URL + tag_a.attrs["href"]

        elif "imagens/exclamacao" in img:

            dict_tags["aviso"] = True

        peticionamento = lista_tags[1].find(src=re.compile("peticionamento"))

        if peticionamento:

            pattern = re.search("\((.*)\)", peticionamento.attrs["onmouseover"])
            dict_tags["peticionamento"] = pattern.group().split('"')[1]

        else:

            dict_tags["peticionamento"] = ""

    processo = lista_tags[2].find("a")

    dict_tags["link"] = URL + processo.attrs["href"]

    dict_tags["numero"] = processo.string

    dict_tags["visualizado"] = (
        True if processo.attrs["class"] == "processoVisualizado" else False
    )

    tag = lista_tags[3].find("a")

    dict_tags["atribuicao"] = tag.string if tag else ""

    dict_tags["tipo"] = lista_tags[4].string

    tag = lista_tags[5].find(class_="spanItemCelula")

    dict_tags["interessado"] = tag.string if tag else ""

    return dict_tags


def tag_controle(tag):
    key, value = "", ""

    img = str(tag.img["src"])

    pattern = re.search("\((.*)\)", tag.attrs.get("onmouseover"))

    if "imagens/sei_anotacao" in img:

        # Separa o texto interno retornado pelo js onmouseover delimitado
        # pelas aspas simples. Salvo somente o primeiro e terceiro items

        value = pattern.group().split("'")[1:4:2]

        key = "postit_red" if "prioridade" in img else "postit"

    elif "imagens/sei_situacao" in img:

        key = "situacao"
        value = pattern.group().split("'")[1]

    elif "imagens/marcador" in img:

        marcador = pattern.group().split("'")[1:4:2]
        key = "marcador"
        value = "".join(marcador)

    elif "imagens/exclamacao" in img:

        key = "aviso"
        value = True

    return key, value


def cria_dict_tags(lista_tags):
    """ Recebe uma lista de tags de cada linha do processo  da página inicial
    do SEI, retorna um dicionário dessas tags
    """

    dict_tags = {key: "" for key in KEYS}

    assert (
        len(lista_tags) == 6
    ), "Verifique o nº de tags de cada linha do \
    processo, valor diferente de 10"

    controles = lista_tags[1].find_all("a")

    for tag in controles:

        controles = {k: v for k, v in tag_controle(tag)}

    dict_tags = {**dict_tags, **controles}

    peticionamento = lista_tags[1].find(src=re.compile("peticionamento"))

    if peticionamento:
        pattern = re.search("\((.*)\)", peticionamento.attrs["onmouseover"])

        dict_tags["peticionamento"] = pattern.group().split('"')[1]

    processo = lista_tags[2].find("a")

    dict_tags["processo"] = processo.string

    atribuicao = lista_tags[3].find("a")

    if atribuicao:
        dict_tags["atribuicao"] = atribuicao.string

    dict_tags["tipo"] = lista_tags[4].string

    interessado = lista_tags[5].find(class_="spanItemCelula")

    if interessado:
        dict_tags["interessado"] = interessado.string

    return dict_tags


def dict_to_df(processos):
    """Recebe a lista processos contendo um dicionário das tags de cada
    processo aberto no SEI. Retorna um Data Frame cujos registros
    são as string das tags.
    """

    cols = [
        "processo",
        "tipo",
        "atribuicao",
        "marcador",
        "anotacao",
        "prioridade",
        "peticionamento",
        "aviso",
        "situacao",
        "interessado",
    ]

    df = pd.DataFrame(columns=cols)

    for p in processos:
        df = df.append(pd.Series(p), ignore_index=True)

    df["atribuicao"] = df["atribuicao"].astype("category")
    df["prioridade"] = df["prioridade"].astype("category")
    df["tipo"] = df["tipo"].astype("category")

    return df


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


def save_page(page, filename):
    with open(filename, "w") as file:
        # html = soup(driver.page_source).prettify()

        # write image
        file.write(page.driver.page_source)

        # TODO: install weasyprint

        # TODO; autoit

    # driver.fechar()


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


def authenticate_google(path_to_file="files/anatel.json"):

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_file, scope)

    return gspread.authorize(credentials)


def load_gsheet(title: str) -> gspread.Spreadsheet:
    """Authenticate the user, opens the Goole Spreadsheet
    
    Arguments:
        title {str} -- Google Drive Spreadsheet Name 

    Raises:
        ValueError  -- if Spreadsheet is not found
    
    Returns:
        gspread.Spreadsheet -- [Google Spreadsheet Object]
    """

    auth = authenticate_google()

    try:

        sheet = auth.open(title=title)

    except gspread.SpreadsheetNotFound:

        raise ValueError(f"Planilha {title} não foi encontrada. Verifique o seu Drive")

    return sheet


def load_wb_from_sheet(title: str, aba: str):
    """Carrega a Planilha Google title e retorna aba
    
    Arguments:
        title {str} -- Nome da Planilha no Google Drive
        aba {str} -- Nome da Aba da Planilha    
    
    Raises:
        ValueError --  if Spreadsheet or Workbook not found
    """

    sh = load_gsheet(title)

    try:

        wb = sh.worksheet(aba)

    except gspread.WorksheetNotFound:

        raise ValueError(
            f" A aba não foi encontrada na Planilha {title}. Verifique o seu Drive"
        )

    return wb


def load_df_from_sheet(title: str, aba: str, skiprows: list = None, **kwargs):
    """Carrega a Planilha Google title e retorna a aba como um Dataframe
    
    Args:
        title (str): Nome da Planilha no Google Drive
        aba (str): Nome da Aba da planilha
        skiprows (list, optional): Defaults to None. Opcionalmente ignora essas linhas. 
    """

    wb = load_wb_from_sheet(title=title, aba=aba)

    df = gs_to_df.get_as_dataframe(
        wb,
        evaluate_formulas=True,
        skiprows=skiprows,
        dtype=str,
        na_values=["nan", ""],
        allow_formulas=True,
    )

    df = df.dropna(axis=0, how="all")

    return df


def load_workbooks_from_drive():
    """
    Receives: tuple of strings

        Authenticate the access to Google Sheets Feed
        Open all authorized Spreadsheets and puts in a list wkbs
        Filter this list to contain only Spreadsheets with in tuple 'criteria'

    Returns:

        A list with Spreadsheet objects containing one of criteria in the title
    """
    gc = authenticate_google()

    return gc.openall()


def salva_aba_no_drive(dataframe, planilha_drive, aba_drive):

    workbook = authenticate_google().open(planilha_drive)

    worksheet = workbook.worksheet(aba_drive)

    worksheet.clear()

    gs_to_df.set_with_dataframe(dataframe=dataframe, worksheet=worksheet, resize=True)


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


def string_endereço(dados, extra=True):
    d = {}

    s = "A(o)<br>"

    s += f'<b>{dados["Nome/Razão Social"].upper()}</b>'

    s += "<br>" + dados["Logradouro"].title() + ", " + dados["Número"] + " "

    s += dados["Complemento"].title() + " "

    s += dados["Bairro"].title() + "<br>"

    s += (
        "CEP: "
        + dados["Cep"]
        + " - "
        + dados["Município"].title()
        + " - "
        + dados["UF"]
    )

    if extra:

        s += "<br><br>" + "<b>FISTEL: " + dados["Fistel"] + "</b>"

        s += "<br>" + "<b>Validade: " + dados["Validade"] + "</b>"

        s += "<br>" + "<b>Indicativo: " + dados["Indicativo"] + "</b>"

        debitos = dados["Entidade Devedora"].upper()

        if debitos == "SIM":
            color = r"#FF0000"
        else:
            color = r"#0000FF"

        s += f'<br><b>Possui débitos? : <span style="color:{color};">{debitos}</span></b>'

    d["À"] = s

    return d


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


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


def add_point(c):
    while len(c) < 11:
        c += "0" + c

    if len(c) == 11:
        return c[:3] + "." + c[3:6] + "." + c[6:9] + "-" + c[9:]

    if len(c) == 14:
        return c[:2] + "." + c[2:5] + "." + c[5:8] + "/" + c[8:12] + "-" + c[12:]

