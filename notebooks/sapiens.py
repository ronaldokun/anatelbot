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

# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataSciece.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass

# %%
import pandas as pd
import os
import gc
import pickle
import numpy as np

from time import sleep

import gspread_dataframe as gs_df

os.chdir("c:/Users/rsilva/gdrive/projects/programming/automation/")

PATH = os.path.join(os.getcwd(), 'files/')

# INITIALIZE DRIVER
from selenium import webdriver
import sapiens
import functions
import sistemas


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

CPF = '33831640807'
PASS_1 = "Fer465023@ur_"
PASS_2 = "Fer465023"


# %%
get_ipython().system('ls {PATH}')

# %% [markdown]
# ### Loga Driver no Sapiens

# %%
def start_sapiens(cpf, senha, db={}):   
   
    page = functions.init_browser(webdriver.Firefox(), 'rsilva', 'Savorthemom3nts')
    
    page = sapiens.LoginPage(page.driver).login(cpf, senha)
    
    page = sapiens.Sapiens(page.driver, db)
        
    return page


# %%
def fix_cpf_cnpj(_id):
    
    if len(_id) in (12, 13, 14):
        
        while len(_id) < 14:
            
            _id = '0' + str(_id)
            
        return _id
            
    elif len(_id) <= 11:
    
        while len(_id) < 11:

            _id = '0' + str(_id)
            
        return _id
    
    return ""

# %%
page = start_sapiens(CPF, PASS_2)

# %% [markdown]
# ### Cria/Carrega o Data Frame para exportar os dados

# %%
database = pd.read_excel(PATH+"planilha_auxiliar_CADIN.xlsx", dtype=str).replace("nan", "")


# %%
database.head()


# %%
database.shape


# %%
database.dropna(inplace=True)


# %%
sapiens_page = start_sapiens(CPF, PASS_2)


# %%
df = pd.DataFrame(columns=sapiens.KEYS)


# %%
counter = 0

for i, row in database.iterrows():
    
    cpf = row["CPF/CNPJ"].replace(".", "").replace('-', "")
    
    cpf = fix_cpf_cnpj(cpf)
    
    if len(cpf) > 11: next
    
    registro = sapiens_page.get_registro(cpf)    
   
    if registro is None:
            
        sapiens_page.pesquisa_dados(cpf)
        
        registro = sapiens_page.get_registro(cpf)
        
        counter += 1
        
    df = df.append(pd.Series(registro), ignore_index=True)
        
    if counter > 100:
        
        df.to_csv("registros_atualizados.csv", index=False)
        
        new = start_sapiens(CPF, PASS_2, sapiens_page.registros) 
        
        sapiens_page.driver.close()
        
        sapiens_page = new
        
        sleep(10)        
                
        counter = 0 
        
        gc.collect()
        
        
else:
    
    df.to_csv("registros_atualizados.csv", index=False)


# %%
df.to_excel("registros_atualizados.xlsx", index=False)


# %%
df["Endereço_Completo"] = df.apply(lambda row: " ".join([str(row["Logradouro"]), 
                                                         str(row["Número"]), 
                                                         str(row["Complemento"]),
                                                         str(row["Bairro"]), "\n", "CEP:", 
                                                         str(row["Cep"]), 
                                                         str(row["Cidade"])]
                                                       ), axis=1
                                  )


# %%
#writer = pd.ExcelWriter("files/planilha_obito.xlsx")
#df.to_excel(writer, "consulta_RF", index=False, encoding='utf-8')
#writer.save()


# %%
#gs_df.set_with_dataframe(registros_rf, df, row=1, include_column_header=True)
#gs_df.set_with_dataframe(registros, pd.DataFrame(df["Nome"]), row=1, col=9, include_column_header=False)
#gs_df.set_with_dataframe(registros, pd.DataFrame(df["Endereço_Completo"]), row=1, col=12, include_column_header=False)


# %%
gs_df.set_with_dataframe(registros, df, row=743, col=14, include_column_header=False)


