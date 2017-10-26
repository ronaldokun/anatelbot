#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldo
"""

from selenium.webdriver.common.by import By


class Login(object):

    URL = "https://sapiens.agu.gov.br/"

    TITLE = "SAPIENS"

    LOGIN = (By.ID, "cpffield-1018-inputEl")

    SENHA = (By.ID, "textfield-1019-inputEl")
    

class Rf(object):
    
    URL = "https://sapiens.agu.gov.br/receitafederal"
    
    IDINPUTCPF = (By.ID, "textfield-1014-inputEl")
    
    RESULTADO = (By.CLASS_NAME, "x-grid-cell-inner")
   
    CPF = (By.ID, "textfield-1014-inputEl")
    
    NAME = (By.ID, "textfield-1015-inputE1")
    
    QUADRO1 = (By.CLASS_NAME, "x-grid-cell-inner")


class Base(object):

    INITIALPAGE = (By.ID, "lnkControleProcessos")

    EXIBIRMENU = (By.ID, "lnkInfraMenuSistema")
    
    NAV_URL = Login.URL + "/sei/"


class LatMenu(object):

    BLOCOASS = (By.LINK_TEXT, "Blocos de Assinatura")


class Main(object):

    FILTROATRIBUICAO = (By.ID, "ancVisualizacao1")

    TIPOVISUALIZACAO = (By.ID, "ancTipoVisualizacao")

    CONTADOR = (By.ID, "selInfraPaginacaoSuperior")


class ListaBlocos(object):

    TITLE = "SEI - Blocos de Assinatura"


class Bloco(object):

    TITLE = "SEI - Documentos do Bloco de Assinatura"


class Processo(object):
    
    TITLE = "SEI - Processo"

    TXT_AND_PRE = "Solicita-se ao protocolo a expedição do "

    TXT_AND_MID = " ( SEI nº "

    TXT_AND_POS = "por meio de correspondência simples com aviso de recebimento."
    
class Envio(object):
    
    TITLE =         "SEI - Selecionar Unidades"
    
    PRAZO =         "3"
    
    IDSIGLA =         (By.ID, "txtSiglaUnidade")
    
    SIGLASEDE =          "Protocolo.Sede"
    
    TXTSEDE =       "Protocolo.Sede - Protocolo da Sede"
    
    IDSEDE =        (By.ID, "chkInfraItem0")
    
    IDBTNTRSP =          (By.ID, "btnTransportarSelecao")
                
    LUPA =          "objLupaUnidades.selecionar(700,500)"
    
    IDUNIDADE =       (By.ID, "txtUnidade")
        
    IDMANTERABERTO =  (By.ID, "chkSinManterAberto")
    
    IDRETDATA =       (By.ID, "optDataCerta")
    
    IDRETDIAS =       (By.ID, "optDias")
    
    IDNUMDIAS =       (By.ID, "txtDias")
    
    IDUTEIS =         (By.ID, "chkSinDiasUteis")
    
    IDENVIAR =        (By.ID, "sbmEnviar")

    
