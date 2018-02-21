
import os

os.chdir(r'C:\Users\rsilva\Google Drive\projects\programming\automation')

import datetime as dt
from time import sleep
from selenium.webdriver.common.by import By
from functions import *
import random

from selenium import webdriver


url = "http://sistemasnet/sarh/horarioflexivelNovo/lancamento/LancamentoHoras.asp?SISQSmodulo=18384"

USER = 'rsilva'
PASS = 'Savorthemom3nts'


def leave(time):

    while time > dt.datetime.now():

        print(dt.datetime.now())

        sleep(60 * random.randint(5,10))

    try:

        import web_scraping_sei

    except:

        print("Problema na emissão dos bloco")

    print("Emissão de Bloco efetuada com sucesso")

    page = init_browser(webdriver=webdriver.Firefox(), login=USER, senha=PASS)

    page.driver.get(url)

    btn = page.wait_for_element_to_click((By.ID, 'image2'))

    btn.click()

    sleep(5)

    try:

        alert = page.alert_is_present(timeout=5)

        alert.accept()


    except:

        print("Entered Except Block on Leave!")

    try:

        alert = page.alert_is_present(timeout=5)

        alert.accept()

        page.close()

    except:

        print("Entered second Except Block")




def enter(time):

    while time > dt.datetime.now():

        print(dt.datetime.now())

        sleep(60 * random.randint(5, 10))

    try:

        import web_scraping_sei

    except:

        pass


    page = init_browser(webdriver=webdriver.Firefox(), login=USER, senha=PASS)

    page.driver.get(url)

    btn = page.wait_for_element_to_click((By.ID, 'image1'))

    btn.click()

    sleep(2)

    try:


        alert = page.alert_is_present(timeout=5)

        if alert:
            alert.accept()

        page.close()


    except:

        print("Entered Except Block in Enter")


entra = dt.datetime(2018, 2, 21, 8,10)

#sai = dt.datetime(2018, 1, 29, 21, 30)

#leave(sai)

enter(entra)

