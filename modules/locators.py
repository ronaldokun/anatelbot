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

    LOG = (By.ID, "txtUsuario")

    PWD = (By.ID, "pwdSenha")


class Base(object):

    INIT = (By.ID, "lnkControleProcessos")

    MENU = (By.ID, "lnkInfraMenuSistema")

    URL = Login.URL + "/sei/"


class LatMenu(object):

    BL_ASS = (By.LINK_TEXT, "Blocos de Assinatura")


class Main(object):
    
    TITLE = 'SEI - Controle de Processos'

    ATR = (By.ID, "ancVisualizacao1")

    VISUAL = (By.ID, "ancTipoVisualizacao")

    CONT = (By.ID, "selInfraPaginacaoSuperior")


class Blocos(object):

    TITLE = "SEI - Blocos de Assinatura"


class Bloco(object):

    TITLE = "SEI - Documentos do Bloco de Assinatura"

    RET_BLOCO = ((By.ID, 'btnExcluir'))


class Tree(object):

    TITLE = "SEI - Processo"
       
class Central(object):
    
    ACOES = (By.ID, "divArvoreAcoes")
    
    IN_AND = (By.ID, "txaDescricao")
    
    SV_AND = (By.ID, "sbmSalvar")
    
    AND_PRE = "Solicita-se ao protocolo a expedição do "

    AND_MID = " ( SEI nº "

    AND_POS = "por meio de correspondência simples com aviso de recebimento."

class Envio(object):
    
    TITLE = "SEI - Enviar Processo"

    UNIDS = "SEI - Selecionar Unidades"

    PRAZO = "3"

    IN_SIGLA = (By.ID, "txtSiglaUnidade")

    SIGLA = "Protocolo.Sede"

    SEDE = "Protocolo.Sede - Protocolo da Sede"

    ID_SEDE = (By.ID, "chkInfraItem0")

    B_TRSP = (By.ID, "btnTransportarSelecao")

    LUPA = "objLupaUnidades.selecionar(700,500)"

    IDUNIDADE = (By.ID, "txtUnidade")

    OPEN = (By.ID, "chkSinManterAberto")

    IDRETDATA = (By.ID, "optDataCerta")

    RET_DIAS = (By.ID, "optDias")

    NUM_DIAS = (By.ID, "txtDias")

    UTEIS = (By.ID, "chkSinDiasUteis")

    ENVIAR = (By.ID, "sbmEnviar")


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
