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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import os
import gc
from pathlib import *

import pandas as pd
import pyperclip as clip # copiar o texto clipboard
from time import sleep
import xlwings as xw

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup

import random

# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")

#import sistemas
import sei.sei as sei 
import functions
import page
from page import *
import sei.sei_helpers as helpers
from sistemas.sistemas import Scpx

% reload_ext autoreload
% autoreload 2

# %%
PATH = os.path.abspath(r"C:\Users\rsilva\Desktop\SEI")
#PATH = os.path.abspath(r"S:\PUBLICO\SCANNER\Scanner - OR")
HOME = os.path.abspath("C:/Users/rsilva/gdrive/projects/programming/automation/")
#DIG = os.path.abspath("S:\PUBLICO\Outorga 3º Andar\Planilhas para acompanhamento de Pagamentos")

# %%
sht = xw.Book(os.path.join(HOME,'files\Analise.xlsm')).sheets("Consulta")
#pg = xw.Book(os.path.join(HOME, "files\pagamentos.xlsm")).sheets("Consulta") 
serv = {'302':'Radioamador', '400':'Rádio do Cidadão', '507': 'Limitado Móvel Aeronáutico', '604': 'Limitado Móvel Marítimo'}

# %%
keys = ('Nome/Razão Social', 'Logradouro', 'Número', 'Complemento', 'Bairro', 'Cep', 'Município', 'UF', 'Número Fistel')

def string_endereço(dados):
    
    d = {}
    
    s = 'A(o)<br>' 
    
    s += dados["Nome/Razão Social"].title()
    
    s += '<br>' + dados["Logradouro"].title() + ", " + dados["Número"] + " " 
    
    s += dados["Complemento"].title() + " " 
    
    s += dados["Bairro"].title() + '<br>' 
    
    s += "CEP: " + dados["Cep"] + " - " + dados["Município"].title() + " - " + dados["UF"] 
            
    s += "<br><br>" + "<b>FISTEL: " + dados["Número Fistel"] + "</b>"
    
    d["A"] = s
    
    return d

def lastRow(ws, col=2):
    """ Find the last row in the worksheet that contains data.

    idx: Specifies the worksheet to select. Starts counting from zero.

    workbook: Specifies the workbook

    col: The column in which to look for the last cell containing data.
    """

    #ws = workbook.sheets[idx]

    lwr_r_cell = ws.cells.last_cell      # lower right cell
    lwr_row = lwr_r_cell.row             # row of the lower right cell
    lwr_cell = ws.range((lwr_row, col))  # change to your specified column

    if lwr_cell.value is None:
        lwr_cell = lwr_cell.end('up')    # go up untill you hit a non-empty cell

    return lwr_cell.row


# %%
usr = "rsilva"
pwd = "Savorthemom3nts"
sei_ = sei.login_sei(webdriver.Firefox(), usr, pwd)

# %%
sei_.itera_processos()

# %%
len(sei_.get_processos())

# %%
last_row = functions.lastRow(sht)
row = 91
cpf = str(sht.cells(row, 2).value)[:11]
#nome = sht.cells(row, 3).value.replace("(", '').replace(")", "").strip()
proc = sht.cells(row, 1).value
servico = serv[str(int(sht.cells(row, 7).value))]
ind = sht.cells(row, 8).value
fistel = sht.cells(row, 10).value
email = sht.cells(row, 16).value
clip.copy(ind)
p = sei_.go_to_processo(proc)


# %%
os.remove(file)
row += 1

# %%
#files = sorted(os.listdir(PATH))
#file = os.path.join(PATH, files[-1])
#os.rename(file, os.path.join(PATH, ind+'.pdf'))
files = sorted(os.listdir(PATH))
file = os.path.join(PATH, file)
#os.rename(file, os.path.join(PATH, ind+'.pdf'))
#files = sorted(os.listdir(PATH))
file = os.path.join(PATH, file)
p.incluir_doc_externo("Folha", file, arvore=Path(file).stem, timeout=10)
p = sei_.go_to_processo(proc)
sleep(5)
os.remove(file)

# %%
files = sorted(os.listdir(PATH))
for file in files[1:]:
    file = os.path.join(PATH, file)

# %%
assunto = 'Serviço {0} - Processo: {1} Boletos {2} - ANATEL/RSAB'.format(servico, proc, ind)

msg = 'E-mail_PPDESS'

p.send_doc_por_email('3721613', (email, assunto, msg), timeout=1)
# %%
p = sei_.go_to_processo(proc)

sleep(0.5)
p.edita_postit()
sleep(1)
p.edita_marcador(tipo="MA - Aguardando AR/Resposta", content='Até 18/01/2019',timeout=1)
#p.excluir_acomp_especial()

#p.concluir_processo()

# %%
row = 99
for i in range(1, 4):

    pg.cells(row+i, 2).value = fistel
    pg.cells(row+i, 3).value = i
    pg.cells(row+i, 4).value = proc
    pg.cells(row+i, 6).value = cpf

# %%
driver = webdriver.Ie()
scpx = Scpx(driver)

# %%
dados = scpx.extrai_cadastro(cpf)

# %%
p.incluir_oficio("RC_OF_Sem_Contexto_PPDESS", string_endereço(dados))

# %%
#windows = sei_.driver.window_handles

#sei_.driver.switch_to_window(windows[0])

sei_.driver.switch_to.default_content()

# %%
analisados = []

for num, p in sei_.get_processos().items():    
   
    if p['atribuicao'] == 'deleicfaria':
    
        proc = sei_.go_to_processo(num)

        tree = proc.armazena_arvore()

        if "Licença" in " ".join(list(tree.keys())):

            analisados.append(p)        


# %%
gc.collect()

# %%
concluidos = analisados[:]

for p in concluidos:    
        
        proc = sei_.go_to_processo(p['numero'])
        
        y = input()
        
        if y == "":

            proc.edita_marcador()
            proc.edita_postit()
            proc.excluir_acomp_especial()
            proc.concluir_processo()
            analisados.remove(p)
            

# %%
concluidos = analisados[:]

for p in analisados:    
        
    proc = sei_.go_to_processo(p['numero'])
    
    tree = proc.armazena_arvore()
    
    if "AR" in str(list(tree.keys())[-1]):
        
        concluidos.append(p)            


# %%
from pathlib import *

src = Path("C:/Users/rsilva/Documents/24.11.18_Piracicaba/Done")
dst = Path("C:/Users/rsilva/Documents/24.11.18_Piracicaba/Scanner")


# %%
src = list(src.iterdir())
dst = list(dst.iterdir())

# %%
proc = "53504.000808/2018-10"

p = sei_.go_to_processo(proc)

for file in src[:1]:
    p.incluir_doc_externo("Folha", str(file), arvore=file.stem, timeout=10)

# %%
src[54]

# %%
proc = "53504.000808/2018-10"
p = sei_.go_to_processo(proc)

# %%



