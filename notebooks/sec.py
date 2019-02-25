# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python [default]
#     language: python
#     name: python3
# ---

# %%
import os
import gc
import pandas as pd
import xlwings as xw
import gspread as gs
import gspread_dataframe as gs_df
from bs4 import BeautifulSoup as soup


# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")

from time import sleep

from sistemas.sistemas import Sec

import functions
from page import *

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

HOME = os.path.abspath("C:/Users/rsilva/gdrive/projects/programming/automation/")


# %%
sht = xw.Book(os.path.join(HOME,'files/prova_botucatu.xlsx')).sheets("interessados")


# %%
df = pd.read_excel(os.path.join(HOME,'files/prova_botucatu.xlsx'), dtype=str)


# %%
df.head()


# %%
caps = DesiredCapabilities.INTERNETEXPLORER

caps['version'] = '11.0'
caps['requireWindowsFocus'] = True
caps['ignoreProtectedModeSettings'] = True

driver = webdriver.Ie(capabilities=caps)
sec = Sec(driver)


# %%
cadastro = pd.DataFrame(columns=SEC_DADOS)

for i, row in df.iterrows():
    
    dados = sec.extrai_cadastro(row['CPF'])
    
    cadastro = cadastro.append(pd.Series({col:dados.get(col) for col in SEC}), ignore_index=True)    
    
    break       


# %%
dados = sec.extrai_cadastro('08180266850', timeout=1)


# %%
KEYS = ["Consultar", "Dados do Usuário", "Dados de Telefones", "Endereço Correspondência", "Endereço Sede", "Certificado", "Não Cadastrado", "Categoria"]

def soup_clean(elem):

    ids = ["ImgObrigatorioIndCertificadoEstrangeiro",
           "msgIndCertificadoEstrangeiro"]

    if 'id' in elem.attrs and elem.attrs['id'] in ids:
        return False
    
    else:

        return True


source = soup(sec.driver.page_source, 'lxml')

values = [l.text.strip().strip(":") for l in source.find_all('label', soup_clean)]

values = [d for d in values if d not in KEYS]


# %%
keys = [l.text.strip().strip(":") for l in source.find_all('td', string=True)]

keys = [k for k in keys if k]


# %%
for elem in source.find_all('label'):
    print(soup_clean(elem))


# %%
sec.imprimir_provas(num_prova='11628', cpf='31888916877', num_registros=122, start=0, end=30)


# %%
dict_ = sec._extrai_inscritos_prova()


# %%
df = pd.DataFrame(columns=['Nome', 'CPF'])

for k,v in dict_.items():
    
    df = df.append(pd.Series({'Nome': v.nome, "CPF": k}), ignore_index=True)
    
df


# %%
df.to_excel("Relação de Inscritos_B.xlsx", index=False)

# %%
for k,v in dict_.items():
    print(k,v)
    break


