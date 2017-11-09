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
    
    RET_BLOCO = ((By.ID, 'btnExcluir'))


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
    
class Boleto(object):
    
    URL = 'http://sistemasnet/boleto/Boleto/ConsultaDebitos.asp?SISQSmodulo=6853'
    
    B_FISTEL = (By.ID, 'indTipoConsulta0')
    
    B_CPF = (By.ID, 'indTipoConsulta1')
    
    INPUT_FISTEL = (By.ID, 'NumFistel')
    
    INPUT_CPF = (By.ID, 'NumCNPJCPF')
    
    INPUT_DATA = (By.ID, 'DataPPDUR')
    
    BUT_CONF = (By.ID, 'botaoFlatConfirmar')
    
    MRK_TODOS = (By.ID, 'botaoFlatMarcarTodos')
    
    PRINT = (By.ID, 'botaoFlatImprimirSelecionados')
    

    
