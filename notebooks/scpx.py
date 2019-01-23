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
import pyperclip as clip
import xlwings as xw
# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")

from time import sleep
from sistemas.sistemas import Scpx
import sei
import functions
from page import *
import selenium.webdriver as webdriver

% reload_ext autoreload
% autoreload 2

serv = {'400': 'Rádio do Cidadão', '302': 'Radioamador', '507': 'Limitado Móvel Aeronáutico', '604': 'Limitado Móvel Marítimo'}

# %%
PATH = os.path.abspath(r"C:\Users\rsilva\Desktop\SEI")
HOME = os.path.abspath("C:/Users/rsilva/gdrive/projects/programming/automation/")
#DIG = os.path.abspath("S:\PUBLICO\Outorga 3º Andar\Planilhas para acompanhamento de Pagamentos")

# %%
sht = xw.Book(os.path.join(HOME,"files/rodrigoca.xlsm")).sheets("Consulta")
#pg = xw.Book(os.path.join(HOME, "files/pagamentos.xlsm")).sheets("Consulta") 

# %%
last_row = functions.lastRow(sht)
row = 70
cpf = str(sht.cells(row, 5).value)[:11]
proc = sht.cells(row, 1).value
#servico = serv[sht.cells(row, 7).value]
fistel = sht.cells(row, 2).value
email = sht.cells(row, 16).value

# %% [markdown]
# # Scpx - Manipulação de Cadastro

# %%
driver = webdriver.Ie()
scpx = Scpx(driver)

# %% [markdown]
# ## Consulta

# %%
scpx.consulta(cpf, timeout=2)

# %% [markdown]
# ## Serviço

# %%
scpx.servico_incluir(cpf, num_processo=proc, silent=True, timeout=1)


# %%
#scpx.servico_excluir(cpf, documento="2724547")
scpx.imprime_consulta(cpf)

# %% [markdown]
# ## Estação

# %%
scpx.prorrogar_rf(cpf)

# %%
scpx.prorrogar_estacao(cpf)

# %%
scpx.incluir_estacao(cpf, 'Fixa', 'PX2D0037', sequencial='001', timeout=3)
# %%
scpx.incluir_estacao(cpf, 'Móvel', 'PX2J5719', sequencial='001', timeout=1)

# %%
scpx.movimento_transferir(cpf, 'A', 'E', proc=proc, timeout=2)

# %%
scpx.movimento_transferir(cpf, 'A', 'G', proc=proc)

# %%
scpx.movimento_cancelar(cpf)

# %%
scpx.licenciar_estacao(cpf, silent=True, timeout=2)

# %%
scpx.licenciar_estacao(cpf, ppdess=False, silent=True, timeout=2)

# %%
dados = scpx.extrai_cadastro(cpf, timeout=1)

# %%
dados

# %% [markdown]
# ## Licença

# %%
scpx.imprimir_licenca(cpf, timeout=3)

# %%
last_row = functions.lastRow(pg)
for i in range(1, 4):

    pg.cells(last_row+i, 2).value = dados['Boleto PPDUR'][:11]
    pg.cells(last_row+i, 3).value = i
    pg.cells(last_row+i, 4).value = proc
    pg.cells(last_row+i, 6).value = cpf

# %%


