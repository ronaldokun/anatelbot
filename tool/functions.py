# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 16:50:19 2017

@author: rsilva
"""
# Basic Bultins
import datetime as dt
import re

from selenium import webdriver

# Third-part Libraries
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions

# TODO: Generalize this
NO_DRIVER = """
You need to install the chromedriver for Selenium\n
Please see this link https://github.com/weskerfoot/DeleteFB#how-to-use-it\n
"""
PADRAO_IND = [
    r"^(P){1}(X){1}(\d){1}([A-Z]){1}(\d){4}$",
    r"^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$",
    r"^(P){1}([A-Z]){4}$",
    r"^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})",
]

STRIP = ("/", ".", "-")

BROWSERS = {
    "chrome": {
        "name": "chrome",
        "instance": webdriver.Chrome,
        "options": ChromeOptions,
    },
    "firefox": {
        "name": "firefox",
        "instance": webdriver.Firefox,
        "options": FirefoxOptions,
    },
    "ie": {"name": "ie", "instance": webdriver.Ie, "options": IeOptions},
    "edge": {"name": "edge", "instance": webdriver.Edge, "options": EdgeOptions},
}


def strip_string(identificador: str, strip: tuple = STRIP) -> str:
    """Remove os caracteres contidos em strip do identificador

    Args:
        identificador (str): String a ser processada
        strip (tuple, optional): Tupla com caracteres a serem removidos. Defaults to STRIP.

    Returns:
        str: String `identificador` formatada.
    """
    return "".join(s for s in identificador if s not in strip)


# TODO: try using seleniumrequests instead
def get_browser(browser: str = "Chrome", is_headless: bool = False):
    """Inicia a instância webdriver com algumas configurações otimizadas
    e com o navegador logado na rede da Anatel

    Args:
        browser (str, optional): [String com o nome do navegador]. Defaults to "Chrome".
        login (str, optional): [Nome do Usuário]. Defaults to None.
        senha (str, optional): [Senha do Usuário]. Defaults to None.
        timeout (int, optional): [Tempo máximo de espera na navegação]. Defaults to 10.

    Returns:
        [webdriver]: [Webdriver instance]
    """
    _browser = BROWSERS.get(browser.lower(), None)
    if not _browser:
        raise ValueError(
            f"O browser mencionado é inválido ou não suportado, use uma dessas opções: {BROWSERS.items()!r}"
        )

    if _browser["name"] != "edge":
        options = _browser["options"]()
        if _browser["name"] == "chrome":
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "disk-cache-size": 4096,
            }
            options.add_experimental_option("prefs", prefs)
            options.add_argument("start-maximized")

        if is_headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("log-level=2")

        driver = _browser["instance"](options=options)
    else:
        driver = _browser["instance"]()

    if not _browser["name"] == "chrome":
        driver.maximize_window()

    return driver


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


# TODO: Remove
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
