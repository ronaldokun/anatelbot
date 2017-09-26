#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldo
"""

from selenium.webdriver.common.by import By


class Login(object):

    URL = "https://sei.anatel.gov.br"

    TITLE = "SEI / ANATEL"

    LOGIN = (By.ID, "txtUsuario")

    SENHA = (By.ID, "pwdSenha")


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
    
    TRSP =          (By.ID, "btnTransportarSelecao")
                
    LUPA =          "objLupaUnidades.selecionar(700,500)"
    
    UNIDADE =       (By.ID, "txtUnidade")
    
    
    MANTERABERTO =  (By.ID, "chkSinManterAberto")
    
    RETDATA =       (By.ID, "optDataCerta")
    
    RETDIAS =       (By.ID, "optDias")
    
    NUMDIAS =       (By.ID, "txtDias")
    
    UTEIS =         (By.ID, "chkSinDiasUteis")
    
    ENVIAR =        (By.ID, "sbmEnviar")

    
