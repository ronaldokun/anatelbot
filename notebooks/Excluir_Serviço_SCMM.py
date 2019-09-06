# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python [conda env:automation]
#     language: python
#     name: conda-env-automation-py
# ---

# %%
import os

os.chdir("C:/Users/rsilva/automation")

from sistemas.sistemas import Slmm
import selenium.webdriver as webdriver

# %reload_ext autoreload
# %autoreload 2

# %%
driver = webdriver.Edge()

# %%
slmm = Slmm(driver)

# %%
PROC = r"53504.0058552019-31"
DOC = "4590866"

nums = """50406218684
50406228809
50406228132
50406228990
50406232245
50406269670
50406269327
50406269599
50405817690
50406272468
50406271810
50406272620
02020748118
""".split()

# %%
from tqdm import tqdm_notebook

for fistel in tqdm_notebook(nums):
    
    try:
        
        #slmm.consulta(fistel,"id_fistel", 2)
        slmm.servico_excluir(fistel, tipo_id="id_fistel", documento=DOC, motivo="Cassação", 
                             num_proc=PROC, timeout=1)
        print(fistel)        
    except:
        pass        

# %%
