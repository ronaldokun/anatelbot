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
import gspread_dataframe as gs
import pyperclip as clip # copiar o texto clipboard
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup

import random

# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")

#import sistemas
from sei import sei
from sei.sei_helpers import *
import page
from page import *
from sistemas import sistemas
import functions

% reload_ext autoreload
% autoreload 2

# %%
def extrai_pares_tabulação(source):
    trs = source.find_all('tr')
    dados = {}
    i = 1
    for tr in trs:        
        td = tr.find_all('td', string=True)
        label = tr.find_all('label', string=True)
        
        i = 1
        for field, result in zip(td, label):
            field, result = field.text[:-1], result.text
            if field in dados:
                field = field + "_" + str(i + 1)
            dados[field] = result 
       
    return dados

# %%
def string_endereço(dados):
    
    d = {}
    
    s = 'A(o)<br>' 
    
    s += dados["Nome/Razão Social"].title()
    
    s += '<br>' + dados["Logradouro"].title() + ", " + dados["Número"] + " " 
    
    s += dados["Complemento"].title() + " " 
    
    s += dados["Bairro"].title() + '<br>' 
    
    s += "CEP: " + dados["Cep"] + " - " + dados["Município"].title() + " - " + dados["UF"] 
            
    s += "<br><br>" + "<b>FISTEL: " + dados["Número Fistel"] + "</b>"
    
    s += "<br><br>" + "<b>Validade: " + dados["Validade Radiofreqüência"] + "</b>"
    
    
    d["À"] = s
    
    #d[r'vencem(ram)'] = 'vencem(ram) em {0}'.format(dado['Validade Radiofreqüência'])
    
    return d

# %%
processo = r'53504.008813/2018-71'

# %%
usr = 'rsilva'
pwd = 'Savorthemom3nts'
sei_ = sei.login_sei(webdriver.Firefox(), usr, pwd)

# %%
sei_.itera_processos()

# %%
p = sei_.go_to_processo(processo)

# %%
auth = functions.authenticate_google("files/anatel.json")
wb = auth.open(title="RC")
sht = wb.worksheet(processo)
df = gs.get_as_dataframe(sht, dtype=str)

# %%
usr = "rsilva"
pwd = "Savorthemom3nts"

page = webdriver.Ie()
scpx = sistemas.Scpx(page)

# %%
validade_rf = sht.range('C2:C53')
fistel = sht.range('c8:c53')

# %%
dados = pd.read_pickle("dados.pkl")

# %%
nomes = []
for v in dados.values():
    nomes.append(v['Nome/Razão Social'])
    
nomes = sorted(nomes)
print(len(nomes), nomes)

# %%
for f in fistel:
    
    f = str(f.value)    
    
    while len(f) < 11:
        f = '0' + f
        
    #dado = dados.get(f, None)
        
    #if dado in (None, ""): 
        
    dado = scpx.extrai_cadastro(f, tipo_id='id_fistel', timeout=5)
        
    dados[f] = dado
        
    pd.to_pickle(dados, "dados.pkl")   
        
                
    p.incluir_oficio("RC_Oficio de Cassação", dados=string_endereço(dados[f]), timeout=5)
    
    p = sei_.go_to_processo(processo)
            
    gc.collect()

# %%
dados[f]

# %%
dados

# %%
#pd.to_pickle(dados, "dados.pkl")
dados = pd.read_pickle("dados.pkl")

# %%
len(dados)

# %%
scpx.movimento_cancelar("05712320860")

# %%
df = pd.DataFrame(columns=dados[0].keys())

# %%
for dic in dados:

    df = df.append(pd.Series(dic), ignore_index=True)
    
df.head()

# %%
vals = []

for i, values in df[df["Processo"] == processo].iterrows():
    fistel = values.FISTEL
    while len(fistel) < 11:
        fistel = '0' + fistel
    scpx.consulta(fistel,tipo_id='id_fistel')
    source = soup(scpx.driver.page_source, "lxml")
    dados = extrai_pares_tabulação(source)
    
    scpx.wait_for_element_to_click((By.ID, "botaoFlatPróximo")).click()
    val_rf = source.find(id='labelDataValidadeRadioFrequencia')
    
    #source = soup(scpx.driver.page_source, "lxml")
    #dados = {**dados, **extrai_pares_tabulação(source)}
                                               
    #proximo = scpx.wait_for_element_to_click((By.ID, "botaoFlatEstação"))
    #proximo.click()
    
    #source = soup(scpx.driver.page_source, "lxml")
    #dados = {**dados, **extrai_pares_tabulação(source)}
    
    print("Nome: {}".format(values['NOME']))
    print("Validade de Radiofrequência: {}".format(val_rf.text))
    print("Data de Validade Licença: {}\n".format(dados['Data Validade Licença']))
    
    vals.append(val_rf) 
    
df.loc[df["Processo"] == processo, "Validade_RF"] = vals
