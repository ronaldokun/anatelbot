
import os

os.chdir(r'C:\Users\rsilva\Google Drive\projects\programming\automation')

import datetime as dt
from time import sleep
from selenium.webdriver.common.by import By
from functions import init_browser
import random




url = "http://sistemasnet/sarh/horarioflexivelNovo/lancamento/LancamentoHoras.asp?SISQSmodulo=18384"



def leave(time):


    while time > dt.datetime.now():

        print(dt.datetime.now())

        sleep(60 * random.randint(5,10))

    page = init_browser()
    page.driver.get(url)

    btn = page.wait_for_element_to_click((By.ID, 'image2'))

    btn.click()

    try:

        alert = page.alert_is_present(timeout=5)

        alert.accept()

    except:

        page.close()

    page.close()

def enter(time):

    while time > dt.datetime.now():

        print(dt.datetime.now())

        sleep(60 * random.randint(10, 20))

    page = init_browser()
    page.driver.get(url)

    btn = page.wait_for_element_to_click((By.ID, 'image1'))

    btn.click()

    alert = page.alert_is_present(timeout=5)

    try:

        alert = page.alert_is_present(timeout=5)

        alert.accept()

    except:

        page.close()

    sleep(30)

    page.close()


entra = dt.datetime(2018, 1, 11, 7)

#sai = dt.datetime(2018, 1, 10, 21, 15)

#leave(sai)

enter(entra)

