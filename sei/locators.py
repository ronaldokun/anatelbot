#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldoS
"""

from selenium.webdriver.common.by import By

class LoginLocators(object):

    URL          = "https://sei.anatel.gov.br"

    TITLE = "SEI / ANATEL"
    
    LOGIN        = (By.ID, "txtUsuario")

    SENHA        = (By.ID, "pwdSenha")

class BaseLocators(object):
    
    INITIALPAGE     = (By.ID, "lnkControleProcessos")

    EXIBIRMENU      = (By.ID, "lnkInfraMenuSistema")

class LatMenuLocators(object):

    BLOCOASS    = (By.LINK_TEXT, "Blocos de Assinatura")
    
class MainLocators(object):
    
    FILTROATRIBUICAO    = (By.ID, "ancVisualizacao1")

    TIPOVISUALIZACAO    = (By.ID, "ancTipoVisualizacao")

    CONTADOR            = (By.ID, "selInfraPaginacaoSuperior")
    
    
class ListaBlocosLocators(object):

    TITLE = "SEI - Blocos de Assinatura"

class BlocoLocators(object):

    TITLE = "SEI - Documentos do Bloco de Assinatura"

class ProcPageLocators(object):
    
    TXT_ANDAM_PRE = "Solicita-se ao protocolo a expedição do Ofício "

    TXT_AND_MID = " ( SEI nº "

    TXT_AND_POS = " ) por meio de correspondência simples com aviso de recebimento"




    
