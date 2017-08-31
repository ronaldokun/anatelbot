#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldoS
"""

from selenium.webdriver.common.by import By


URL = "https://sei.anatel.gov.br"

LOGOUT_TITLE = "SEI / ANATEL"

LISTA_BLS_TITLE = "SEI - Blocos de Assinatura"

BLOCO_TITLE = "SEI- Documentos do Bloco de Assinatura"

LOGIN = (By.ID, "txtUsuario")

SENHA = (By.ID, "pwdSenha")

FILTROATRIBUICAO = (By.ID, "ancVisualizacao1")

TIPOVISUALIZACAO = (By.ID, "ancTipoVisualizacao")

INITIALPAGE = (By.ID, "lnkControleProcessos")

CONTADOR = (By.ID, "selInfraPaginacaoSuperior")

EXIBIRMENU = (By.ID, "lnkInfraMenuSistema")

BLOCOASS = (By.LINK_TEXT, "Blocos de Assinatura")
    
