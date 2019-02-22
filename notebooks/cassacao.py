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
#     display_name: Python [conda env:automation]
#     language: python
#     name: conda-env-automation-py
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
import sei.sei as sei
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
processo = r'53504.000636/2019-65'

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
df.shape

# %%
usr = "rsilva"
pwd = "Savorthemom3nts"

page = webdriver.Ie()
scpx = sistemas.Scpx(page)

# %%
nome = df['Nome da Entidade'][1:]
cpf = df['CNPJ/CPF'][1:]
fistel = df['Fistel'][1:]

# %%
#dados = pd.read_pickle("dados.pkl")

# %%
dados = pd.read_pickle("dados.pkl")


for i, (n, f, c) in enumerate(zip(nome, fistel, cpf)):
    
    f = str(f)
    
    p = sei_.go_to_processo(processo)

    sleep(5)
    
    while len(f) < 11:
        f = '0' + f
        
    dado = dados.get(c, None)    
        
    if not dado: 
        
        dado = scpx.extrai_cadastro(f, tipo_id='id_fistel', timeout=5)
        
        dados[c] = dado
        
        pd.to_pickle(dados, "dados.pkl")
        
    val = dado['Validade Radiofreqüência']
        
    df.loc[df["CNPJ/CPF"] == c, "Validade"] = val
    
    print(dado["Nome/Razão Social"], val)
                
    #tags = sei_.pesquisa_contato(n)
    
    #if tags is None:
        
    #    sei_._cria_contato(dado)
        
    #else:
        
    #    try:
    #        sei_._mudar_dados_contato(dado)            
    #    except: next
    
    p.incluir_oficio("RC_Oficio de Cassação", dados=string_endereço(dados[c]), timeout=5)
    
    sleep(5)
    
    gc.collect()

# %%
dados.keys()

# %%
df.Validade = pd.to_datetime(df['Validade'])

# %%
df.loc[df.Validade >= '2019', ['CNPJ/CPF', 'Nome da Entidade', 'Fistel', 'Validade']]

# %%
gs.set_with_dataframe(sht, df)

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
