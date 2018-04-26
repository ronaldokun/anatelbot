import os

import xlwings as xw

# Change the directory to reflect the main repository
os.chdir("../")

import sistemas
from page import *

BROWSER = None

def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets["SCPX"].range("A1").value = "Hello xlwings!"


def inicia_analise():

    if not BROWSER:

        BROWSER = sistemas.Scpx(webdriver.Ie())

        return BROWSER

@xw.func
def hello(name):
    return "hello {0}".format(name)
