import os


import xlwings as xw
import sistemas as s
import sei
import functions as f
from page import *



def hello_xlwings():
    wb = xw.Book.caller()
    sh = wb.sheets.active


@xw.func
def hello(name):
    return "hello {0}".format(name)
