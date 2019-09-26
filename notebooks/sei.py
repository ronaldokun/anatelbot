# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.3
#   kernelspec:
#     display_name: Python [conda env:anatel]
#     language: python
#     name: conda-env-anatel-py
# ---

# +
#Standard Lib imports
import sys, os
from pathlib import Path
#from functools import partial
import getpass

# Insert in Path Project Directory
sys.path.insert(0, str(Path().cwd().parent))


# Third party imports

# Local application imports
from sei import sei

#USR = getpass.getuser()
USR = 'rsilva'
print(f'Olá {USR}')
PWD = getpass.getpass("Digite sua Senha: ")

# %load_ext autoreload
# %autoreload 2
# -

s = sei.login_sei(USR, PWD, browser='Firefox', timeout=5, teste=False)

s.mudar_lotação("GR01")

s.mudar_lotação("GR01FI3")

s.mudar_lotação("GR01AF")

s.ver_detalhado()

s.is_init_page()

s.go_to_init_page()

s.show_lat_menu()

s.page.timeout = 2

s.ver_detalhado()

s.ver_todos()

s.itera_processos()

s.get_processos()

s.go_to_blocos()

num = "53504.009880/2019-93"
p = s.go_to_processo(num)

p.is_open()

p.incluir_documento('Externo')

p.page.timeout = 2

p.send_doc_por_email('0177520', ('ronaldokun@gmail.com', "Teste", "Medição RFeye"))

p.abrir_pastas()

p._get_acoes('0177509')

p.is_open()

/html/body/div[1]/div[3]/div[1]/form/div[4]/table/tbody/tr[3]/td[2]

/html/body/div[1]/div[3]/div[1]/form/div[4]/table/tbody/tr[2]/td[2]
