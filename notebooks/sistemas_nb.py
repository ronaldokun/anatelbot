
#%%
import os
import gc
import xlwings as xw
import pandas as pd

# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")

from time import sleep

import sistemas
import sei
import functions
import page
from page import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver as webdriver

get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


#%%
usr = "rsilva"
pwd = "Savorthemom3nts"

caps = DesiredCapabilities.INTERNETEXPLORER

caps['version'] = '11.0'
caps['requireWindowsFocus'] = True
caps['ignoreProtectedModeSettings'] = True

driver = webdriver.Ie(capabilities=caps)


#%%
scpx = sistemas.Scpx(driver)


#%%
cpf = '80113267673'


#%%
cpf = cpf.replace(".","").replace('-',"").replace("/", "")


#%%
scpx.consulta(cpf, tipo_id='id_fistel')


#%%
scpx.servico_incluir(cpf)


#%%
scpx.incluir_estacao(cpf, 'Móvel', 'PX2M1986')


#%%
scpx.consulta(cpf)


#%%
scpx.movimento_aprovar(cpf, 'B')


#%%
scpx.licenciar_estacao(cpf, ppdess=True)


#%%
scpx.licenciar_estacao(cpf, ppdess=False)


#%%
os.listdir("files/csv")


#%%
import pandas as pd

registros = pd.read_csv("files/Expedidos.csv", dtype=str)
registros.fillna("", inplace=True)


#%%
registros.head()


#%%
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


#%%
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup

for f in registros[registros["Processo"] == '53504.008730/2018-81'].iterrows():
    fistel = f[1].Fistel
    while len(fistel) < 11:
        fistel = '0' + fistel
    scpx.consulta(fistel,tipo_id='id_fistel')
    source = soup(scpx.driver.page_source, "lxml")
    dados = extrai_pares_tabulação(source)
    
    scpx.wait_for_element_to_click((By.ID, "botaoFlatServiço")).click()
    val_rf = source.find(id='labelDataValidadeRadioFrequencia')
    
    #source = soup(scpx.driver.page_source, "lxml")
    #dados = {**dados, **extrai_pares_tabulação(source)}
                                               
    proximo = scpx.wait_for_element_to_click((By.ID, "botaoFlatEstação"))
    proximo.click()
    
    #source = soup(scpx.driver.page_source, "lxml")
    #dados = {**dados, **extrai_pares_tabulação(source)}
    
    print("Nome: {}".format(f[1]['Nome']))
    print("Validade de Radiofrequência: {}".format(val_rf.text))
    print("Data de Validade Licença: {}\n".format(dados['Data Validade Licença']))
    
    dados = {}


#%%
scpx.close()
gc.collect()


#%%
for k,v in dados.items():
    print("{} : {}".format(k,v))


#%%
database = pd.DataFrame()


#%%
for v in banco_de_dados.values():
    db = pd.DataFrame([v])
    
    database = database.append(db)


#%%
database.head()


#%%
scpx.incluir_serviço(CPF)


#%%
scpx.aprovar_movimento(CPF, "B")


#%%
scpx.licenciar_estacao(CPF)


#%%
scpx.consulta(CPF)


#%%
datas = ["23052018", "24052018"]
horas = ["1300", "1400"]

horarios = [(dia,hora) for dia in datas for hora in horas][2:]

print(horarios)

sistemas.abrir_agenda_prova(browser, horarios)


