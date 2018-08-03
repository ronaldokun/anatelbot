#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldo
"""

from collections import namedtuple

from selenium.webdriver.common.by import By

SISTEMASNET = 'http://sistemasnet/'

class Sapiens(object):

    URL = "https://sapiens.agu.gov.br/"

    TITLE = "SAPIENS"

    LOGIN = (By.ID, "cpffield-1017-inputEl")

    SENHA = (By.ID, "textfield-1018-inputEl")

class Rf_Sapiens(object):

    URL = "https://sapiens.agu.gov.br/receitafederal"

    BTN_PF = (By.ID, "tab-1083-btnInnerE1")

    BTN_PJ = (By.ID, "tab-1084-btnInnertE1")

    ID_INPUT_CPF = (By.ID, "textfield-1014-inputEl")

    ID_INPUT_CNPJ = (By.ID, "textfield-1051-inputEl")

    RESULTADO = (By.CLASS_NAME, "x-grid-cell-inner")

    CPF = (By.ID, "textfield-1014-inputEl")

    NAME = (By.ID, "textfield-1015-inputE1")

class Sei(object):

    Login = namedtuple('Login', 'url, title, log, pwd')("https://sei.anatel.gov.br",
                                                        "SEI / ANATEL",
                                                        (By.ID, "txtUsuario"),
                                                        (By.ID, "pwdSenha"))

    Base = namedtuple('Base', 'init, menu, url, pesquisa')((By.ID, "lnkControleProcessos"),
                                                           (By.ID, "lnkInfraMenuSistema"),
                                                           "https://sei.anatel.gov.br/sei/",
                                                           (By.ID, "txtPesquisaRapida"))

    Oficio = namedtuple('Oficio', 'editor, top_frame, iframes, submit')((By.ID, "frmEditor"),
                                                                            (By.ID, "cke_4_top"),
                                                                            (By.CLASS_NAME, "cke_wysiwyg_frame cke_reset"),
                                                                            (By.ID, "cke_129"))

class Menu_lateral(object):

    CLT_PROC = (By.LINK_TEXT, "Controle de Processos")

    INIT_PROC = (By.LINK_TEXT, "Iniciar Processo")

    RET_PROG = (By.LINK_TEXT, "Retorno Programado")

    PESQ = (By.LINK_TEXT, "Pesquisa")

    BASE_KNW = (By.LINK_TEXT, "Base de Conhecimento")

    TXT_PDR = (By.LINK_TEXT, "Textos Padrão")

    MDL_FAV = (By.LINK_TEXT, "Modelos Favoritos")

    BL_ASS = (By.LINK_TEXT, "Blocos de Assinatura")

    BL_REU = (By.LINK_TEXT, "Blocos de Reunião")

    BL_INT = (By.LINK_TEXT, "Blocos Internos")

    CONTS = (By.LINK_TEXT, "Contatos")

    CONTS_LISTAR = (By.LINK_TEXT, 'Listar')

    SOBRS = (By.LINK_TEXT, "Processos Sobrestados")

    AC_ESP = (By.LINK_TEXT, "Acompanhamento Especial")

    MRKS = (By.LINK_TEXT, "Marcadores")

    PT_CTRL = (By.LINK_TEXT, "Pontos de Controle")

class Sei_Inicial(object):

    TITLE = 'SEI - Controle de Processos'

    ATR = (By.ID, "ancVisualizacao1")

    VISUAL = (By.ID, "ancTipoVisualizacao")

    CONT = (By.ID, "selInfraPaginacaoSuperior")

class Blocos(object):

    TITLE = "SEI - Blocos de Assinatura"

class Bloco(object):

    TITLE = "SEI - Documentos do Bloco de Assinatura"

    RET_BLOCO = ((By.ID, 'btnExcluir'))

class Proc_incluir(object):

    TITLE = "SEI - Processo"

    ESPEC = (By.ID, 'txtDescricao')

    INTER = (By.ID, 'txtInteressadoProcedimento')

    SIG = (By.ID, 'optSigiloso')

    REST = (By.ID, 'optRestrito')

    PUBL = (By.ID, 'optPublico')

    HIP_LEGAL = (By.ID, 'selHipoteseLegal')

    HIPS = ['',
            'Controle Interno (Art. 26, § 3º, da Lei nº 10.180/2001)',
            'Direito Autoral (Art. 24, III, da Lei nº 9.610/1998)',
            'Documento Preparatório (Art. 7º, § 3º, da Lei nº 12.527/2011)',
            'Fiscalização / Investigação da Anatel (Art. 174 da Lei nº 9.472/1997)',
            'Informação Pessoal (Art. 31 da Lei nº 12.527/2011)',
            'Informações Contábeis de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
            'Informações Econômico-Financeiras de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
            'Informações Operacionais de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
            'Informações Privilegiadas de Sociedades Anônimas (Art. 155, § 2º, da Lei nº 6.404/1976)',
            'Informações Técnicas de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
            'Interceptação de Comunicações Telefônicas (Art. 8º, caput, da Lei nº 9.296/1996)',
            'Investigação de Responsabilidade de Servidor (Art. 150 da Lei nº 8.112/1990)',
            'Livros e Registros Contábeis Empresariais (Art. 1.190 do Código Civil)',
            'Operações Bancárias (Art. 1º da Lei Complementar nº 105/2001)',
            'Proteção da Propriedade Intelectual de Software (Art. 2º da Lei nº 9.609/1998)',
            'Protocolo -Pendente Análise de Restrição de Acesso (Art. 6º, III, da Lei nº 12.527/2011)',
            'Segredo de Justiça no Processo Civil (Art. 189 do Código de Processo Civil)',
            'Segredo de Justiça no Processo Penal (Art. 201, § 6º, do Código de Processo Penal)',
            'Segredo Industrial (Art. 195, XIV, Lei nº 9.279/1996)',
            'Sigilo das Comunicações (Art. 3º, V, da Lei nº 9.472/1997)',
            'Sigilo de Empresa em Situação Falimentar (Art. 169 da Lei nº 11.101/2005)',
            'Sigilo do Inquérito Policial (Art. 20 do Código de Processo Penal)',
            'Situação Econômico-Financeira de Sujeito Passivo (Art. 198, caput, da Lei nº 5.172/1966 - CTN)'
            ]

    #BTN_SALVAR = (By.CLASS_NAME, "cke_button cke_button__save cke_button_disabled")

class Proc_central(object):

    ACOES = (By.ID, "divArvoreAcoes")

    IN_POSTIT = (By.ID, "txaDescricao")

    BT_POSTIT = (By.NAME, "sbmRegistrarAnotacao")

    CHK_PRIOR = (By.ID, "chkSinPrioridade")

    #OPT_MARCADORES = (By.CLASS_NAME, "dd-pointer dd-pointer-down")

    SV_AND = (By.ID, "sbmSalvar")

    AND_PRE = "Solicita-se ao protocolo a expedição do "

    AND_MID = " ( SEI nº "

    AND_POS = "por meio de correspondência simples com aviso de recebimento."

class Marcador(object):

    SELECT_MARCADOR = (By.ID, "selMarcador")

    LISTA_MARCADORES = (By.CLASS_NAME, "dd-options dd-click-off-close")

    TXT_MARCADOR = (By.ID, "txaTexto")

    SALVAR = (By.NAME, "sbmGerenciarMarcador")

class Acompanhamento_Especial(object):

    GRUPOS = (By.ID, "selGrupoAcompanhamento")

    TXT = (By.ID, "txaObservacao")

    SALVAR = (By.NAME, "sbmCadastrarAcompanhamento")

    EXCLUIR = (By.ID, "btnExcluir")

class Envio(object):

    TITLE = "SEI - Enviar Processo"

    UNIDS = "SEI - Selecionar Unidades"

    PRAZO = "5"

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

class Criar_Processo(object):

    EXIBE_ALL = (By.ID, 'imgExibirTiposProcedimento')

    FILTRO = (By.ID, 'txtFiltro')

    SL_TIP_PROC = (By.ID, "selTipoProcedimento")

    PROCS = {'',
             'Acesso à Informação: Demanda do e-SIC',
             'Acompanhamento Competição: Monitoramento Mercados',
             'Acompanhamento da Ordem Econômica: Anuência Prévia',
             'Acompanhamento da Ordem Econômica: Aprovação Posterior',
             'Acompanhamento da Ordem Econômica: Ato de Concentração',
             'Acompanhamento da Ordem Econômica: Condicionamentos',
             'Acompanhamento da Ordem Econômica: Proposta de Grupo PMS',
             'Acompanhamento da Ordem Econômica: Registro de Alterações Contratuais ou do Estatuto Social',
             'Acompanhamento da Ordem Econômica: Revisão de Grupo PMS',
             'Acompanhamento Econômico: Estudo de AIR',
             'Acompanhamento Econômico: RAEC',
             'Acompanhamento Legislativo: Câmara dos Deputados',
             'Acompanhamento Legislativo: Congresso Nacional',
             'Acompanhamento Legislativo: Estadual/Distrital',
             'Acompanhamento Legislativo: Municipal',
             'Acompanhamento Legislativo: Senado Federal',
             'Anuências: Bens Reversíveis',
             'Anuências: Contratos Vinculados à Concessão',
             'Aquisição: Adesão a Ata de RP-Não Participante',
             'Aquisição: Adesão a Ata de RP-Participante',
             'Aquisição: Aplicação de Sanção decorrente de Procedimento Licitatório',
             'Aquisição: Concorrência',
             'Aquisição: Concorrência-Registro de Preço',
             'Aquisição: Concurso',
             'Aquisição: Consulta',
             'Aquisição: Convite',
             'Aquisição: Coordenação das Gerências Regionais',
             'Aquisição: Dispensa - Acima de R$ 8 mil',
             'Aquisição: Dispensa - Até R$ 8 mil',
             'Aquisição: Inexigibilidade',
             'Aquisição: Leilão',
             'Aquisição: Plano de Aquisições',
             'Aquisição: Pregão Eletrônico',
             'Aquisição: Pregão Eletrônico-Registro de Preço',
             'Aquisição: Pregão Presencial',
             'Aquisição: Regime Diferenciado de Contratação-RDC',
             'Aquisição: Tomada de Preços',
             'Arrecadação: Compensação',
             'Arrecadação: Controle de Depósito Judicial',
             'Arrecadação: Cumprimento de Ação Judicial',
             'Arrecadação: Encaminhamento para Dívida Ativa',
             'Arrecadação: Normatização Interna',
             'Arrecadação: Notificação/Comunicado de Cobrança',
             'Arrecadação: Parcelamento Administrativo',
             'Arrecadação: Parcelamento do Programa de Regularização de Débitos (PRD)',
             'Arrecadação: Receita',
             'Arrecadação: Regularização de Indébitos',
             'Arrecadação: Restituição',
             'Arrecadação: Restituição/Compensação',
             'Arrecadação: Retificação de Declaração - Fust',
             'Arrecadação: Subsidiar Ação Judicial',
             'CADE: Indícios de Infração à Ordem Econômica',
             'CADE: Subsídios',
             'Certificação de Produto: Alteração de Escopo de Laboratório',
             'Certificação de Produto: Alteração de Escopo de OCD',
             'Certificação de Produto: Auditoria de Laboratório',
             'Certificação de Produto: Auditoria de OCD',
             'Certificação de Produto: Autorização de Ensaios em Laboratórios de Ordem Inferior de Prioridade',
             'Certificação de Produto: Autorização para Teste Piloto de Produto',
             'Certificação de Produto: Designação de OCD',
             'Certificação de Produto: Habilitação de Laboratório',
             'Certificação de Produto: Homologação',
             'Certificação de Produto: Monitoramento de Produto',
             'Certificação de Produto: Requisitos Técnicos',
             'Comunicação: Demanda de Comunicação',
             'Comunicação: Evento Institucional Público Externo',
             'Comunicação: Evento Institucional Público Interno',
             'Comunicação: Pedido de Apoio Institucional',
             'Comunicação: Plano Anual de Comunicação',
             'Comunicação: Publicidade Institucional',
             'Comunicação: Publicidade Legal',
             'Conselho Consultivo: Deliberações Gerais',
             'Conselho Consultivo: Organização de Reunião',
             'Conselho Diretor: Deliberações Gerais',
             'Conselho Diretor: Organização de Reunião',
             'Consumidor: Avaliação Técnica do SAC de Operadora',
             'Consumidor: Canais de Atendimento da Anatel',
             'Consumidor: Comitês de Defesa dos Consumidores',
             'Consumidor: Conselho de Usuários de Serviços',
             'Consumidor: Coordenação das Gerências Regionais',
             'Consumidor: Diagnóstico da Prestação de Serviço',
             'Consumidor: Divulgação de Informações',
             'Consumidor: Indicador de Atendimento',
             'Consumidor: Interação Institucional',
             'Consumidor: Pesquisa de Opinião',
             'Consumidor: Pesquisa Qualidade',
             'Consumidor: Pesquisa Satisfação',
             'Consumidor: Tratamento de Solicitações',
             'Consumidor: Tratamento Preventivo e Corretivo',
             'Contabilidade: Análise Contábil',
             'Contabilidade: Cadastro e Habilitação no SIAFI',
             'Contabilidade: Conformidade de Gestão',
             'Contabilidade: Contratos e Garantias',
             'Contabilidade: Declarações Diversas',
             'Contabilidade: Designação/Dispensa Responsável no SIAFI',
             'Contabilidade: DIRF',
             'Contabilidade: Encerramento do Exercício',
             'Contabilidade: Fechamento Contábil - Estoque',
             'Contabilidade: Fechamento Contábil Patrimonial',
             'Contabilidade: Manuais',
             'Contabilidade: Normatização Interna',
             'Contabilidade: Prestação de Contas',
             'Controle de Obrigações: Coordenação das Gerências Regionais',
             'Convênios/Ajustes: Acompanhamento da Execução',
             'Convênios/Ajustes: Formalização/Alteração com Repasse',
             'Convênios/Ajustes: Formalização/Alteração sem Repasse',
             'Corregedoria: Análise Prescricional de Processo',
             'Corregedoria: Avaliação para Estabilidade',
             'Corregedoria: Correição',
             'Corregedoria: Investigação Preliminar',
             'Corregedoria: Procedimento Geral',
             'Corregedoria: Processo Administrativo Disciplinar',
             'Corregedoria: Sindicância Punitiva',
             'Demanda Externa: Cidadão (Pessoa Física)',
             'Demanda Externa: Deputado Estadual/Distrital',
             'Demanda Externa: Deputado Federal',
             'Demanda Externa: Judiciário',
             'Demanda Externa: Ministério Público Estadual',
             'Demanda Externa: Ministério Público Federal',
             'Demanda Externa: Órgãos Governamentais Estaduais',
             'Demanda Externa: Órgãos Governamentais Federais',
             'Demanda Externa: Órgãos Governamentais Municipais',
             'Demanda Externa: Outras Entidades Privadas',
             'Demanda Externa: Outros Órgãos Públicos',
             'Demanda Externa: Senador',
             'Demanda Externa: Vereador/Câmara Municipal',
             'Direito de Exploração: Assuntos Regulatórios',
             'Direito de Exploração: Satélite Brasileiro',
             'Direito de Exploração: Satélite Estrangeiro',
             'Espectro: Coordenação Internacional',
             'Espectro: Coordenação Nacional',
             'Espectro: Internalização de Decisão',
             'Espectro: Notificação de Estações Terrestres, Marítimas e Costeiras',
             'Finanças: Execução Financeira',
             'Finanças: Normatização Interna',
             'Finanças: Reembolso/Ressarcimento',
             'Finanças: Relatório de Gestão',
             'Fiscalização Regulatória: Fiscalização e Controle',
             'Fiscalização: Ampliação de Acesso',
             'Fiscalização: Área de Cobertura',
             'Fiscalização: Canais de Atendimento ao Consumidor',
             'Fiscalização: Certificação de Produtos',
             'Fiscalização: Clandestinidade',
             'Fiscalização: Cobrança de Serviços',
             'Fiscalização: Compromissos Assumidos em Anuências Prévias',
             'Fiscalização: Conteúdo de Serviços de Radiodifusão',
             'Fiscalização: Continuidade',
             'Fiscalização: Coordenação das Gerências Regionais',
             'Fiscalização: Demandas sobre Grandes Eventos',
             'Fiscalização: Econômico',
             'Fiscalização: Estudos e Avaliações',
             'Fiscalização: Infraestrutura e Funcionamento de Redes',
             'Fiscalização: Lacração, Apreensão e Interrupção',
             'Fiscalização: Massificação de Acesso',
             'Fiscalização: Oferta e Contratação de Serviços',
             'Fiscalização: Outorga',
             'Fiscalização: Portabilidade Numérica',
             'Fiscalização: Processo de Guarda',
             'Fiscalização: Qualidade',
             'Fiscalização: Radiomonitoração de Satélites',
             'Fiscalização: Reclamação de Radiointerferência',
             'Fiscalização: Relacionamento Pós-Venda',
             'Fiscalização: SeAC e Serviços de TVC/DTH/MMDS',
             'Fiscalização: Termo de Ajustamento de Conduta (TAC)',
             'Fiscalização: Tributário',
             'Fiscalização: Universalização',
             'Fiscalização: Uso do Espectro e Órbita e Recursos de Numeração',
             'Gestão da Informação: Análise de Dados do Setor',
             'Gestão da Informação: Anulação de Ato Administrativo',
             'Gestão da Informação: Arrecadação',
             'Gestão da Informação: Avaliação de Documentos',
             'Gestão da Informação: Controle de Malote',
             'Gestão da Informação: Coordenação das Gerências Regionais',
             'Gestão da Informação: Credenciamento de Segurança',
             'Gestão da Informação: Disponibilizar Dados do Setor',
             'Gestão da Informação: Gestão Documental',
             'Gestão da Informação: Normatização Interna',
             'Gestão da Informação: Reconstituição Documental',
             'Gestão da Informação: Rol Anual de Informações Classificadas',
             'Gestão da Informação: Segurança da Informação e Comunicações',
             'Gestão de Contrato: Acompanhamento da Execução',
             'Gestão de Contrato: Alterações Contratuais',
             'Gestão de Contrato: Aplicação de Sanção Contratual',
             'Gestão de Contrato: Consultas à PFE-Anatel',
             'Gestão de Contrato: Execução de Garantia',
             'Gestão de Contrato: Orientações e Diretrizes Gerais',
             'Gestão de Contrato: Pagamento Direto a Terceiros',
             'Gestão de Contrato: Processo de Pagamento',
             'Gestão de Processos: Mapeamento e Modelagem',
             'Gestão de Projetos: Planejamento e Execução',
             'Gestão de TI: CITI',
             'Gestão de TI: Coordenação das Gerências Regionais',
             'Gestão de TI: Demanda de Solução de TI',
             'Gestão e Controle: Coordenação - Demandas Externas',
             'Gestão e Controle: Coordenação - Demandas Internas',
             'Gestão e Controle: Demandas de Órgãos de Controle',
             'Gestão e Controle: Executar Auditoria Interna',
             'Gestão e Controle: Plano Anual de Auditoria Interna',
             'Gestão e Controle: Relatório Anual de Auditoria Interna',
             'Homologação de Contratos: Compartilhamento',
             'Homologação de Contratos: Interconexão',
             'Homologação de Contratos: MVNO (Credenciada)',
             'Homologação de Contratos: ORPA',
             'Infraestrutura: Abastecimento de Água e Esgoto',
             'Infraestrutura: Apoio de Engenharia Civil',
             'Infraestrutura: Fornecimento de Energia Elétrica',
             'Institucional: Relatório Anual da Anatel',
             'Licitação: Chamamento Público',
             'Licitação: Concessão',
             'Licitação: Direito de Exploração de Satélite',
             'Licitação: Espectro',
             'Licitação: Espectro - Radiotáxi',
             'Licitação: Espectro - SME',
             'Licitação: Espectro - SMP',
             'Licitação: Numeração',
             'Material: Desfazimento de Material de Consumo',
             'Material: Desfazimento de Material Permanente',
             'Material: Inventário de Material de Consumo',
             'Material: Inventário de Material Permanente',
             'Material: Movimentação de Material de Consumo',
             'Material: Movimentação de Material Permanente',
             'Modelo de Custos: Modelo Bottom-up',
             'Modelo de Custos: Modelo Top-down',
             'Numeração: Atribuição, Destinação e Designação',
             'Numeração: Gestão e Administração',
             'Órbita: Coordenação e Notificação de Redes de Satélite',
             'Orçamento: Acompanhamento de Despesa Mensal',
             'Orçamento: Contingenciamento',
             'Orçamento: Créditos Adicionais',
             'Orçamento: Descentralização de Créditos',
             'Orçamento: Manuais',
             'Orçamento: Programação Orçamentária',
             'Outorga: Autocadastramento',
             'Outorga: Autorização de Uso de Radiofrequência',
             'Outorga: Autorização de Uso de Radiofrequência - Prorrogação',
             'Outorga: Cassação de Autorização',
             'Outorga: Coordenação das Gerências Regionais',
             'Outorga: Dispensa de Autorização',
             'Outorga: Licenciamento de Estação',
             'Outorga: Licenciamento de Estações com Uso de Radiofrequência',
             'Outorga: Limitado Móvel Aeronáutico',
             'Outorga: Limitado Móvel Marítimo',
             'Outorga: Procedimento Simplificado de Outorga',
             'Outorga: Rádio do Cidadão',
             'Outorga: Radioamador',
             'Outorga: Radiotelefonista',
             'Outorga: SCM',
             'Outorga: SeAC',
             'Outorga: Serviços Auxiliares de Radiodifusão e Correlatos (SARC)',
             'Outorga: SLE',
             'Outorga: SLP',
             'Outorga: SLP Especial de Radioautocine',
             'Outorga: SLP Especial de Radiochamada',
             'Outorga: SLP Especial de Supervisão e Controle',
             'Outorga: SLP Limitado - Estações Itinerantes',
             'Outorga: SLP Limitado de Fibras Óticas',
             'Outorga: SLP Limitado Móvel Privativo',
             'Outorga: SLP Limitado Privado de Radiochamada',
             'Outorga: SLP Rádio-Táxi',
             'Outorga: SLP Serviço Limitado Especializado',
             'Outorga: SMP',
             'Outorga: SMP - MVNO',
             'Outorga: STFC',
             'Outorga: Uso Temporário do Espectro',
             'Ouvidoria: Análise Crítica da Anatel',
             'Ouvidoria: Estudo Temático',
             'Ouvidoria: Pesquisa de Satisfação da Anatel',
             'PAC: Acessibilidade - Universalização',
             'PAC: Alteração Societária',
             'PAC: Atendimento',
             'PAC: Banda Larga - PNBL',
             'PAC: Banda Larga nas Escolas - PBLE',
             'PAC: Bens de Terceiros e Serviços Contratados Vinculados à Concessão',
             'PAC: Bens Reversíveis',
             'PAC: Campanhas de Divulgação - Universalização',
             'PAC: Cancelamento de Serviço',
             'PAC: Carregamento de Canais - SeAC',
             'PAC: Casos Críticos',
             'PAC: Cobrança',
             'PAC: Compromisso de Abrangência - SMP',
             'PAC: Compromisso de Aquisição de Produtos e Sistemas Nacionais',
             'PAC: Concessão de Créditos',
             'PAC: Condicionamentos de Atos',
             'PAC: Conta Vinculada à Concessão (RCBR)',
             'PAC: Demanda de Acompanhamento e Controle da Prestação de Serviço',
             'PAC: Direito dos Consumidores',
             'PAC: Disponibilidade e Funcionamento de TUP',
             'PAC: Home Passed - SeAC',
             'PAC: Indicadores de Qualidade',
             'PAC: Interconexão',
             'PAC: Interrupções Sistêmicas',
             'PAC: Invasão de Cobertura',
             'PAC: Meios de Pagamento e Pontos de Venda - TUP',
             'PAC: Numeração',
             'PAC: Obrigações de Qualidade',
             'PAC: Obrigações Gerais',
             'PAC: Oferta de Serviço',
             'PAC: Ônus Contratual da Autorização',
             'PAC: Ônus Contratual da Concessão',
             'PAC: Plano de Melhoria do SMP',
             'PAC: Plano de Seguros do Contrato de Concessão',
             'PAC: Planos de Serviço',
             'PAC: Portabilidade Numérica',
             'PAC: Ressarcimento',
             'PAC: Serviço de Utilidade Pública',
             'PAC: TFF, PPDUR e PPDESS',
             'PAC: Universalização',
             'PADO: Acessibilidade',
             'PADO: Alteração Societária',
             'PADO: Atendimento - Convergente',
             'PADO: Atendimento - SCM',
             'PADO: Atendimento - SeAC',
             'PADO: Atendimento - SMP',
             'PADO: Atendimento - STFC',
             'PADO: Banda Larga - PNBL',
             'PADO: Banda Larga nas Escolas - PBLE',
             'PADO: Bens Reversíveis',
             'PADO: Cancelamento de Serviço - Convergente',
             'PADO: Cancelamento de Serviço - SCM',
             'PADO: Cancelamento de Serviço - SeAC',
             'PADO: Cancelamento de Serviço - SMP',
             'PADO: Cancelamento de Serviço - STFC',
             'PADO: Carregamento de Canais',
             'PADO: Carregamento de Canais - SeAC',
             'PADO: Certificação de Produtos',
             'PADO: Certificação e Não Outorgado - Radiofrequência',
             'PADO: Certificação e Não Outorgado - Serviço',
             'PADO: Certificação e Não Outorgado - Serviço e Radiofrequência',
             'PADO: Co-billing',
             'PADO: Cobrança - Convergente',
             'PADO: Cobrança - SCM',
             'PADO: Cobrança - SeAC',
             'PADO: Cobrança - SMP',
             'PADO: Cobrança - STFC',
             'PADO: Código de Seleção da Prestadora (CSP)',
             'PADO: Competição',
             'PADO: Compromisso de Abrangência - SMP',
             'PADO: Compromisso de Aquisição de Produtos e Sistemas Nacionais',
             'PADO: Descumprimento de Determinação',
             'PADO: Descumprimentos de Condicionamentos de Atos',
             'PADO: Direitos do Consumidor - Convergente',
             'PADO: Direitos do Consumidor - SCM',
             'PADO: Direitos do Consumidor - SeAC',
             'PADO: Direitos do Consumidor - SMP',
             'PADO: Direitos do Consumidor - STFC',
             'PADO: Disponibilidade e Funcionamento de TUP',
             'PADO: Exploração Industrial de Linha Dedicada',
             'PADO: Gestão da Qualidade (PGMQ) - SeAC',
             'PADO: Gestão da Qualidade (RGQ) - SCM',
             'PADO: Gestão da Qualidade (RGQ) - SMP',
             'PADO: Gestão da Qualidade (RGQ) - STFC',
             'PADO: Home Passed - SeAC',
             'PADO: Inadimplemento de TFF, PPDUR e PPDESS',
             'PADO: Interconexão',
             'PADO: Interrupções Sistêmicas - SCM',
             'PADO: Interrupções Sistêmicas - SeAC',
             'PADO: Interrupções Sistêmicas - SMP',
             'PADO: Interrupções Sistêmicas - STFC',
             'PADO: Irregularidade Técnica',
             'PADO: Irregularidade Técnica e Certificação',
             'PADO: Licenciamento de Estação',
             'PADO: LTOG',
             'PADO: Má-fé de Controlador ou Administrador',
             'PADO: Meios de Pagamento e Pontos de Venda - TUP',
             'PADO: Não Outorgado - Radiofrequência',
             'PADO: Não Outorgado - Serviço',
             'PADO: Não Outorgado - Serviço e Radiofrequência',
             'PADO: Numeração',
             'PADO: Obrigações Legais e Contratuais',
             'PADO: Obstrução à Fiscalização',
             'PADO: Oferta de Serviço - Convergente',
             'PADO: Oferta de Serviço - SCM',
             'PADO: Oferta de Serviço - SeAC',
             'PADO: Oferta de Serviço - SMP',
             'PADO: Oferta de Serviço - STFC',
             'PADO: Ônus Contratual da Autorização',
             'PADO: Ônus Contratual da Concessão',
             'PADO: Operação fora do prazo',
             'PADO: Organismo de Certificação Designado (OCD)',
             'PADO: Plano de Seguros do Contrato de Concessão',
             'PADO: Planos de Serviço - Convergente',
             'PADO: Planos de Serviço - SCM',
             'PADO: Planos de Serviço - SeAC',
             'PADO: Planos de Serviço - SMP',
             'PADO: Planos de Serviço - STFC',
             'PADO: Portabilidade Numérica',
             'PADO: Rede Externa',
             'PADO: Remuneração de Redes',
             'PADO: Ressarcimento - Convergente',
             'PADO: Ressarcimento - SCM',
             'PADO: Ressarcimento - SeAC',
             'PADO: Ressarcimento - SMP',
             'PADO: Ressarcimento - STFC',
             'PADO: Rito Sumário',
             'PADO: SAC - Convergente',
             'PADO: SAC - SCM',
             'PADO: SAC - SeAC',
             'PADO: SAC - SMP',
             'PADO: SAC - STFC',
             'PADO: Serviço de Utilidade Pública',
             'PADO: Tarifação - Convergente',
             'PADO: Tarifação - SCM',
             'PADO: Tarifação - SeAC',
             'PADO: Tarifação - SMP',
             'PADO: Tarifação - STFC',
             'PADO: Transferência Irregular de Outorga',
             'PADO: Universalização',
             'PAF: CFRP',
             'PAF: Fust',
             'PAF: TFF',
             'PAF: TFI',
             'PAI: Aspectos Não-Técnicos/Conteúdo',
             'Patrimônio: Cobrança de Acervo Bibliográfico',
             'Patrimônio: Gestão de Acervo Bibliográfico',
             'Patrimônio: Gestão de Bens Imóveis',
             'PD&I: Gestão do Funttel',
             'Pessoal: Abono Permanência - Concessão',
             'Pessoal: Abono Permanência - Revisão',
             'Pessoal: Adicional de Férias (1/3 constitucional)',
             'Pessoal: Adicional de Insalubridade',
             'Pessoal: Adicional de Periculosidade',
             'Pessoal: Adicional Noturno',
             'Pessoal: Adicional por Atividade Penosa',
             'Pessoal: Adicional por Serviço Extraordinário',
             'Pessoal: Adicional por Tempo de Serviço',
             'Pessoal: Afastamento para Atividade Desportiva',
             'Pessoal: Afastamento para Curso de Formação',
             'Pessoal: Afastamento para Depor',
             'Pessoal: Afastamento para Exercer Mandato Eletivo',
             'Pessoal: Afastamento para Pós-Graduação',
             'Pessoal: Afastamento para Serviço Eleitoral (TRE)',
             'Pessoal: Afastamento para servir como Jurado',
             'Pessoal: Afastamento para servir em Organismo Internacional',
             'Pessoal: Afastamento Pós-graduação - com ônus',
             'Pessoal: Afastamento Pós-graduação - sem ônus',
             'Pessoal: Ajuda de Custo com Mudança de Domicílio',
             'Pessoal: Aposentadoria - Concessão',
             'Pessoal: Aposentadoria - Contagem Tempo de Serviço',
             'Pessoal: Aposentadoria - Pensão Temporária',
             'Pessoal: Aposentadoria - Pensão Vitalícia',
             'Pessoal: Aposentadoria - Revisão',
             'Pessoal: Apresentação de Certificado de Curso',
             'Pessoal: Assentamento Funcional do Servidor',
             'Pessoal: Ausência em razão de Casamento',
             'Pessoal: Ausência para Alistamento Eleitoral',
             'Pessoal: Ausência para Doação de Sangue',
             'Pessoal: Ausência por Falecimento de Familiar',
             'Pessoal: Auxílio Acidente',
             'Pessoal: Auxílio Alimentação/Refeição',
             'Pessoal: Auxílio Assistência Pré-Escolar/Creche',
             'Pessoal: Auxílio Doença',
             'Pessoal: Auxílio Funeral',
             'Pessoal: Auxílio Moradia',
             'Pessoal: Auxílio Natalidade',
             'Pessoal: Auxílio Reclusão',
             'Pessoal: Auxílio-Transporte',
             'Pessoal: Avaliação de Desempenho Individual',
             'Pessoal: Avaliação de Desempenho Institucional',
             'Pessoal: Avaliação de Estágio Probatório',
             'Pessoal: Averbação de Tempo de Serviço',
             'Pessoal: Bolsa de Estudo de Idioma Estrangeiro',
             'Pessoal: Bolsa de Pós-Graduação',
             'Pessoal: Cadastro de Dependente no Imposto de Renda',
             'Pessoal: Cessão de Servidor para outro Órgão',
             'Pessoal: Coleta de Imagem de Assinatura',
             'Pessoal: Concurso Público - Exames Admissionais',
             'Pessoal: Concurso Público - Organização',
             'Pessoal: Concurso Público - Provas e Títulos',
             'Pessoal: Controle de Frequência/Abono de Falta',
             'Pessoal: Controle de Frequência/Cumprir Hora Extra',
             'Pessoal: Controle de Frequência/Folha de Ponto',
             'Pessoal: Curso de Pós-Graduação',
             'Pessoal: Curso no Exterior - com ônus',
             'Pessoal: Curso no Exterior - ônus limitado',
             'Pessoal: Curso no Exterior - sem ônus',
             'Pessoal: Curso Promovido pela própria Instituição',
             'Pessoal: Curso Promovido por outra Instituição',
             'Pessoal: Delegação de Competência',
             'Pessoal: Desconto da Contribuição para o INSS',
             'Pessoal: Desconto de Contribuição Associativa',
             'Pessoal: Desconto de Contribuição Sindical',
             'Pessoal: Desconto de Empréstimo Consignado',
             'Pessoal: Desconto de Pensão Alimentícia',
             'Pessoal: Desconto do IRPF Retido na Fonte',
             'Pessoal: Emissão de Certidões e Declarações',
             'Pessoal: Emissão de Procuração',
             'Pessoal: Encargo Patronal - Contribuição para INSS',
             'Pessoal: Estágio - Dossiê do Estagiário',
             'Pessoal: Estágio - Frequência/Folha de Ponto',
             'Pessoal: Estágio - Processo Seletivo',
             'Pessoal: Estágio de Servidor no Brasil',
             'Pessoal: Estágio de Servidor no Exterior',
             'Pessoal: Exoneração de Cargo Efetivo',
             'Pessoal: Falecimento de Servidor',
             'Pessoal: Férias - Alteração',
             'Pessoal: Férias - Interrupção',
             'Pessoal: Férias - Solicitação',
             'Pessoal: Ficha Financeira',
             'Pessoal: Folha de Pagamento',
             'Pessoal: Gratificação de Desempenho',
             'Pessoal: Gratificação Natalina (Décimo Terceiro)',
             'Pessoal: Gratificação por Encargo - Curso/Concurso',
             'Pessoal: Horário de Expediente - Definição',
             'Pessoal: Horário de Expediente - Escala de Plantão',
             'Pessoal: Horário de Expediente - Redução de Jornada',
             'Pessoal: Horário Especial - Familiar Deficiente',
             'Pessoal: Horário Especial - Instrutor de Curso',
             'Pessoal: Horário Especial - Servidor Deficiente',
             'Pessoal: Horário Especial - Servidor Estudante',
             'Pessoal: Indenização de Transporte (meio próprio)',
             'Pessoal: Licença Adotante',
             'Pessoal: Licença Gestante',
             'Pessoal: Licença para Atividade Política',
             'Pessoal: Licença para Capacitação',
             'Pessoal: Licença para Mandato Classista',
             'Pessoal: Licença para Serviço Militar',
             'Pessoal: Licença para Tratamento da Própria Saúde',
             'Pessoal: Licença para Tratar de Interesses Particulares',
             'Pessoal: Licença Paternidade',
             'Pessoal: Licença por Acidente em Serviço',
             'Pessoal: Licença por Afastamento do Cônjuge',
             'Pessoal: Licença por Doença em Pessoa da Família',
             'Pessoal: Licença por Doença Profissional',
             'Pessoal: Licença Prêmio por Assiduidade',
             'Pessoal: Licenças por Aborto/Natimorto',
             'Pessoal: Movimentação de Servidor',
             'Pessoal: Movimento Reivindicatório',
             'Pessoal: Negociação Sindical e Acordo Coletivo',
             'Pessoal: Nomeação/Exoneração de Cargo Comissionado e Designação/Dispensa de Substituto',
             'Pessoal: Normatização Interna',
             'Pessoal: Ocupação de Imóvel Funcional',
             'Pessoal: Orientações e Diretrizes Gerais',
             'Pessoal: Pagamento de Provento',
             'Pessoal: Pagamento de Remuneração',
             'Pessoal: Penalidade Advertência',
             'Pessoal: Penalidade Cassação de Aposentadoria',
             'Pessoal: Penalidade Demissão de Cargo Efetivo',
             'Pessoal: Penalidade Destituição Cargo em Comissão',
             'Pessoal: Penalidade Disponibilidade',
             'Pessoal: Penalidade Suspensão',
             'Pessoal: Pensão por Morte de Servidor',
             'Pessoal: Planejamento da Força de Trabalho',
             'Pessoal: Plano de Capacitação',
             'Pessoal: Prêmios de Reconhecimento',
             'Pessoal: Processo Seletivo para Ocupação de Cargo',
             'Pessoal: Progressão e Promoção (Quadro Efetivo)',
             'Pessoal: Progressão e Promoção (Quadro Específico)',
             'Pessoal: Provimento - Nomeação para Cargo Efetivo',
             'Pessoal: Provimento - Nomeação para Cargo em Comissão',
             'Pessoal: Provimento - por Aproveitamento',
             'Pessoal: Provimento - por Readaptação',
             'Pessoal: Provimento - por Recondução',
             'Pessoal: Provimento - por Reintegração',
             'Pessoal: Provimento - por Reversão',
             'Pessoal: Relação com Conselho Profissional',
             'Pessoal: Remoção a Pedido - Concurso Interno',
             'Pessoal: Remoção a Pedido com Mudança de Sede',
             'Pessoal: Remoção a Pedido para Acompanhar Cônjuge',
             'Pessoal: Remoção a Pedido por Motivo de Saúde',
             'Pessoal: Remoção a Pedido sem Mudança de Sede',
             'Pessoal: Remoção de Ofício com Mudança de Sede',
             'Pessoal: Remoção de Ofício sem Mudança de Sede',
             'Pessoal: Requisição de Servidor Externo',
             'Pessoal: Requisição de Servidor Interno',
             'Pessoal: Ressarcimento ao Erário',
             'Pessoal: Restruturação de Cargos e Funções',
             'Pessoal: Retribuição por Cargo em Comissão',
             'Pessoal: Salário-Família',
             'Pessoal: Saúde - Atestado de Comparecimento',
             'Pessoal: Saúde - Auxílio-Saúde GEAP',
             'Pessoal: Saúde - Cadastro de Dependente Estudante no Auxílio-Saúde',
             'Pessoal: Saúde - Exclusão de Auxílio-Saúde',
             'Pessoal: Saúde - Lançamento Mensal do Auxílio-Saúde no SIAPE',
             'Pessoal: Saúde - Pagamento de Auxílio-Saúde',
             'Pessoal: Saúde - Pagamento de Retroativo',
             'Pessoal: Saúde - Ressarcimento ao Erário',
             'Pessoal: Saúde - Solicitação de Auxílio-Saúde',
             'Pessoal: Saúde e QVT',
             'Pessoal: Subsidiar Ação Judicial',
             'Pessoal: Vacância - Posse em Cargo Inacumulável',
             'Peticionamento: Intercorrente - Processo Novo Relacionado',
             'Planejamento da Fiscalização: Diretrizes',
             'Planejamento da Fiscalização: Plano Anual',
             'Planejamento da Fiscalização: Plano Operacional',
             'Planejamento Estratégico: Acompanhamento do Plano Operacional',
             'Planejamento Estratégico: Agenda Regulatória',
             'Planejamento Estratégico: Análise de Cenários',
             'Planejamento Estratégico: Elaboração do Plano Estratégico',
             'Planejamento Estratégico: Elaboração do Plano Operacional',
             'Planejamento Estratégico: Elaborar Cenários',
             'Planejamento Estratégico: Gestão de Risco',
             'Planejamento Estratégico: Gestão do Plano Estratégico',
             'Planejamento Estratégico: Inteligência Estratégica',
             'Planejamento Estratégico: Monitorar Ambiente',
             'Planos de Serviço: Acompanhamento de Plano do STFC',
             'Planos de Serviço: Gestão de Ofertas e Promoções',
             'Planos de Serviço: Gestão de Planos de Serviço',
             'Planos de Serviço: Homologação de Plano do STFC',
             'Procedimento Administrativo: Acessibilidade',
             'Procedimento Administrativo: Alteração Societária',
             'Procedimento Administrativo: Atendimento',
             'Procedimento Administrativo: Cancelamento de Serviço',
             'Procedimento Administrativo: Carregamento de Canais - SeAC',
             'Procedimento Administrativo: Cobrança',
             'Procedimento Administrativo: Controle de Fiscalização',
             'Procedimento Administrativo: Direito dos Consumidores',
             'Procedimento Administrativo: Inspeção Técnica',
             'Procedimento Administrativo: Interconexão',
             'Procedimento Administrativo: Invasão de Cobertura',
             'Procedimento Administrativo: Numeração',
             'Procedimento Administrativo: Obrigações Gerais',
             'Procedimento Administrativo: Oferta de Serviço',
             'Procedimento Administrativo: Ônus Contratual da Autorização',
             'Procedimento Administrativo: Ônus Contratual da Concessão',
             'Procedimento Administrativo: Portabilidade Numérica',
             'Procedimento Administrativo: Prestação de Informações',
             'Procedimento Administrativo: Ressarcimento',
             'Procedimento Administrativo: TFF, PPDUR e PPDESS',
             'Radiação Restrita: Cadastro de Estação',
             'Radiodifusão: Alteração de Plano Básico',
             'Radiodifusão: Alteração de Plano Básico - Outros',
             'Radiodifusão: Alteração de Plano Básico FM - Alteração de Coordenadas',
             'Radiodifusão: Alteração de Plano Básico FM - Aumento de Potência',
             'Radiodifusão: Alteração de Plano Básico FM - Inclusão de Canal',
             'Radiodifusão: Alteração de Plano Básico FM - Mudança de Canal',
             'Radiodifusão: Alteração de Plano Básico FM - Outras',
             'Radiodifusão: Alteração de Plano Básico OM',
             'Radiodifusão: Alteração de Plano Básico RadCom',
             'Radiodifusão: Alteração de Plano Básico TV - Alteração de Coordenadas',
             'Radiodifusão: Alteração de Plano Básico TV - Aumento de Potência',
             'Radiodifusão: Alteração de Plano Básico TV - Inclusão de Canal',
             'Radiodifusão: Alteração de Plano Básico TV - Mudança de Canal',
             'Radiodifusão: Alteração de Plano Básico TV - Outras',
             'Radiodifusão: Alteração de Plano Básico TV - Redução de Potência',
             'Radiodifusão: Alteração de Plano Básico TV - Retransmissora Auxiliar',
             'Radiodifusão: Alteração Técnica',
             'Radiodifusão: Autocadastramento',
             'Radiodifusão: Autorização de Uso de Radiofrequência',
             'Radiodifusão: Autorização para Instalação de Estação Retransmissora Auxiliar',
             'Radiodifusão: Licenciamento de Estações',
             'Regulamentação: Análise de Impacto Regulatório',
             'Regulamentação: Análise de Proposta Normativa',
             'Regulamentação: Arrecadação',
             'Regulamentação: Cálculo de Preço Público',
             'Regulamentação: Certificação de Produto',
             'Regulamentação: Conselhos e Comitês',
             'Regulamentação: Exploração de Satélite',
             'Regulamentação: Geral do Consumidor',
             'Regulamentação: Numeração',
             'Regulamentação: Órgãos Internacionais',
             'Regulamentação: Pesquisas de Qualidade/Satisfação',
             'Regulamentação: Projetos Especiais',
             'Regulamentação: Proposição de Ato Normativo',
             'Regulamentação: Proposição de Edital de Licitação',
             'Regulamentação: Radiodifusão',
             'Regulamentação: Universalização/Ampliação Acesso',
             'Regulamentação: Uso de Radiofrequências',
             'Relacionamento Institucional: Celebração de Cooperação com outras Instituições',
             'Relacionamento Institucional: Gestão do Relacionamento',
             'Relacionamento Institucional: Participação e Representação em Eventos',
             'Relações Internacionais: Composição de Delegação - com ônus',
             'Relações Internacionais: Composição de Delegação - ônus limitado',
             'Relações Internacionais: Composição de Delegação - sem ônus',
             'Relações Internacionais: Cooperação Internacional',
             'Relações Internacionais: Gestão do GC-CBC',
             'Relações Internacionais: Internalização de Decisão',
             'Relações Internacionais: Proposta de Contribuição',
             'Resolução de Conflitos: Arbitragem Comum',
             'Resolução de Conflitos: Arbitragem em Interconexão',
             'Resolução de Conflitos: Comissão de Resolução de Conflitos das Agência Reguladoras',
             'Resolução de Conflitos: Mediação',
             'Resolução de Conflitos: PGMC',
             'Resolução de Conflitos: Reclamação Administrativa',
             'Revisão de PADO: De Ofício',
             'Revisão de PADO: Mediante Pedido do Interessado',
             'Segurança Institucional: Automação e Controle Predial',
             'Segurança Institucional: Controle de Acesso/Garagem',
             'Segurança Institucional: Controle de Acesso/Portaria',
             'Segurança Institucional: Prevenção contra Incêndio',
             'Segurança Institucional: Projeto contra Incêndio',
             'Segurança Institucional: Serviço de Vigilância',
             'Serviços: Cessão de Uso de Espaço da Anatel',
             'Suporte à Fiscalização: Celebração de Convênios',
             'Suporte à Fiscalização: Gestão de Kits de Fiscalização',
             'Suporte à Fiscalização: Instrumentos e Sistemas',
             'Suporte à Fiscalização: Normas',
             'Suporte à Fiscalização: Planejamento de Aquisições',
             'Suprimento de Fundos: Concessão e Prestação de Contas',
             'Suprimento de Fundos: Solicitação de Despesa',
             'TAC: Abertura de Procedimento para Firmar TAC',
             'TAC: Atendimento',
             'TAC: Banda Larga - PNBL',
             'TAC: Banda Larga nas Escolas - PBLE',
             'TAC: Cancelamento de Serviço',
             'TAC: Certificação de Produtos',
             'TAC: Cobrança',
             'TAC: Compromisso de Abrangência - SMP',
             'TAC: Decumprimentos de Condicionamentos de Atos',
             'TAC: Direitos dos Consumidores',
             'TAC: Disponibilidade e Funcionamento de TUP',
             'TAC: Gestão da Qualidade (RGQ/PGMQ)',
             'TAC: Home Passed - SeAC',
             'TAC: Interrupções Sistêmicas',
             'TAC: Irregularidade Técnica',
             'TAC: Irregularidade Técnica e Obstrução',
             'TAC: Licenciamento de Estação',
             'TAC: Múltiplas Matérias',
             'TAC: Não Outorgado',
             'TAC: Obstrução à Fiscalização',
             'TAC: Oferta de Serviço',
             'TAC: Outras Obrigações Legais e Contratuais',
             'TAC: Planos de Serviço',
             'TAC: Rede Externa',
             'TAC: Ressarcimento',
             'TAC: Tarifação',
             'TAC: Universalização',
             'Tarifas e Preços: Acompanhar Tarifas e Preços',
             'Tarifas e Preços: Cálculo do Fator X',
             'Tarifas e Preços: Cálculo do Índice',
             'Tarifas e Preços: Homologação Tarifas',
             'Tarifas e Preços: Reajuste de Preço',
             'Tarifas e Preços: Reajuste de Tarifa',
             'Tarifas e Preços: Revisão de Tarifa',
             'Universalização/Ampliação do Acesso: Acompanhamento de Políticas Públicas',
             'Universalização/Ampliação do Acesso: Análise de Impacto Regulatório',
             'Universalização/Ampliação do Acesso: Contratações',
             'Universalização/Ampliação do Acesso: Estudos',
             'Universalização/Ampliação do Acesso: Interação Institucional',
             'Universalização: Acessibilidade',
             'Universalização: Acompanhamento do Fust',
             'Universalização: PGMU',
             'Universalização: PMU',
             'Universalização: Proposta de uso do Fust',
             'Viagem: Exterior - Prestação de Contas',
             'Viagem: No País - Prestação de Contas',
             'Viagem: Publicação de Boletim'
             }

class Gerar_Doc(object):

    TIPOS = ("Externo",
             "Ofício",
             "Informe")

    EXTERNO_TIPOS = ("Boleto",
                     "E-mail",
                     "Relação",
                     "Relatório",
                     "Licença")


    doc_externo = dict(id_tipo=(By.ID, 'selSerie'),
                       id_data=(By.ID, 'txtDataElaboracao'),
                       id_txt_tree=(By.ID, 'txtNumero'),
                       id_nato=(By.ID, 'optNato'),
                       id_digit=(By.ID, 'optDigitalizado'),
                       id_pub=(By.ID, "optPublico"),
                       id_restrito=(By.ID, "optRestrito"),
                       id_hip_legal=(By.ID, "selHipoteseLegal"),
                       id_file_upload=(By.ID, "filArquivo"),
                       submit = (By.ID, "btnSalvar"))

    oficio = dict(id_txt_padrao=(By.ID, "optTextoPadrao"),
                  id_modelos=(By.ID, "selTextoPadrao"),
                  id_descricao=(By.ID, 'txtDescricao'),
                  id_dest = (By.ID, "txtDestinatario"),
                  id_pub=(By.ID, "optPublico"),
                  id_restrito = (By.ID, "optRestrito"),
                  id_hip_legal = (By.ID, "selHipoteseLegal"),
                  submit=(By.ID, "btnSalvar"))

    TEXTOS_PADRAO = ['Arquivamento de processo no SEI',
                     'Arquivamento de processo no SEI',
                     'Ato de Cassação - Radioamador',
                     'Ato de Cassação - Radioamador',
                     'ATO DE CASSAÇÃO DO SLP-019',
                     'ATO DE CASSAÇÃO DO SLP-019',
                     'ATO DE CASSAÇÃO DO SLP-028',
                     'ATO DE CASSAÇÃO DO SLP-028',
                     'Ato_RD_GRs_autorizacao_tx',
                     'Ato_RD_GRs_autorizacao_tx',
                     'Ato_RD_GRs_consolidacaotecnica',
                     'Ato_RD_GRs_consolidacaotecnica',
                     'Ato_RD_GRs_enquadramento_pb',
                     'Ato_RD_GRs_enquadramento_pb',
                     'Ato_RD_GRs_homologacao_estudio',
                     'Ato_RD_GRs_homologacao_estudio',
                     'DESPACHO DE ARQUIVAMENTO',
                     'DESPACHO DE ARQUIVAMENTO',
                     'E-mail_(TFI, PPDUR, etc)',
                     'E-mail_(TFI, PPDUR, etc)',
                     'E-Mail_Cancelamento de Serviço',
                     'E-Mail_Cancelamento de Serviço',
                     'E-mail_Exigência',
                     'E-mail_Exigência',
                     'E-mail_Licença/Coer',
                     'E-mail_Licença/Coer',
                     'E-mail_PPDESS',
                     'E-mail_PPDESS',
                     'Edital SLP licenças a vencer',
                     'Edital SLP licenças a vencer',
                     'E_mail_Atualização_Cadastral',
                     'E_mail_Atualização_Cadastral',
                     'Informe de Cassação RA',
                     'Informe de Cassação RA',
                     'Informe de Cassação RC',
                     'Informe de Cassação RC',
                     'Informe de cassação SLP 019',
                     'Informe de cassação SLP 019',
                     'Informe de cassação SLP 028',
                     'Informe de cassação SLP 028',
                     'Informe_Cancelamento_de_PPDESS',
                     'Informe_Cancelamento_de_PPDESS',
                     'Informe_Cancelamento_por_óbito_coletivo',
                     'Informe_Cancelamento_por_óbito_coletivo',
                     'Informe_prescrição_modelo_sede',
                     'Informe_prescrição_modelo_sede',
                     'MA_Boletos_Emissão_Licença',
                     'MA_Boletos_Emissão_Licença',
                     'MA_Cancelamento_Serviço',
                     'MA_Cancelamento_Serviço',
                     'MA_Envio_de_Licença',
                     'MA_Envio_de_Licença',
                     'MA_Exigência',
                     'MA_Exigência',
                     'MA_PPDESS',
                     'MA_PPDESS',
                     'MM_Boletos_Emissão_Licença',
                     'MM_Boletos_Emissão_Licença',
                     'MM_Cancelamento_Serviço',
                     'MM_Cancelamento_Serviço',
                     'MM_Envio_de_Licença',
                     'MM_Envio_de_Licença',
                     'MM_Exigência',
                     'MM_Exigência',
                     'MM_PPDESS',
                     'MM_PPDESS',
                     'OF. DE NOT. CASSAÇÃO SLP028',
                     'OF. DE NOT. CASSAÇÃO SLP028',
                     'OF. DE NOT. RF A VENCER 019',
                     'OF. DE NOT. RF A VENCER 019',
                     'Of. Not. Val. Vencida RA',
                     'Of. Not. Val. Vencida RA',
                     'Oficio cancelamento serviço SLP sem RF',
                     'Oficio cancelamento serviço SLP sem RF',
                     'Oficio de interesse',
                     'Oficio de interesse',
                     'Ofício decisão do Ato 019',
                     'Ofício decisão do Ato 019',
                     'ofício decisão do ato 028',
                     'ofício decisão do ato 028',
                     'Oficio_sócio indébito',
                     'Oficio_sócio indébito',
                     'Of_GERAL_Boletos por Email',
                     'Of_GERAL_Boletos por Email',
                     'Of_GERAL_Envio_Licença_Email',
                     'Of_GERAL_Envio_Licença_Email',
                     'Of_GERAL_PPDESS_Email',
                     'Of_GERAL_PPDESS_Email',
                     'Of_Impugnacao_Debitos',
                     'Of_Impugnacao_Debitos',
                     'Of_Justiça',
                     'Of_Justiça',
                     'Of_Modelo_1',
                     'Of_Modelo_1',
                     'Of_SLP_Exigência_CCadastro',
                     'Of_SLP_Exigência_CCadastro',
                     'RA_Boletos_Emissão_Licença',
                     'RA_Boletos_Emissão_Licença',
                     'RA_Cancelamento_Serviço',
                     'RA_Cancelamento_Serviço',
                     'RA_Declínio de Responsável pela estação',
                     'RA_Declínio de Responsável pela estação',
                     'RA_Envio_COER',
                     'RA_Envio_COER',
                     'RA_Envio_Licença',
                     'RA_Envio_Licença',
                     'RA_Envio_Licença_COER',
                     'RA_Envio_Licença_COER',
                     'RA_Esclarecimento_Classe_D',
                     'RA_Esclarecimento_Classe_D',
                     'RA_Estação Repetidora_PF',
                     'RA_Estação Repetidora_PF',
                     'RA_Exigência',
                     'RA_Exigência',
                     'RA_Exigencia_Prova',
                     'RA_Exigencia_Prova',
                     'RA_PPDESS',
                     'RA_Repetidora Abaixo 200 km',
                     'RA_Repetidora Abaixo 200 km',
                     'RA_Repetidora Indef._PF',
                     'RA_Repetidora Indef._PF',
                     'RC_Oficio de Cassação',
                     'RC_OF_Boletos_Emissão_Licença',
                     'RC_OF_Cancelamento_Serviço',
                     'RC_OF_Cancelamento_Serviço',
                     'RC_OF_Envio_Licença',
                     'RC_OF_Envio_Licença',
                     'RC_OF_Exigência',
                     'RC_OF_Exigência',
                     'RC_OF_PPDESS',
                     'RC_OF_Sem_Contexto_PPDESS',
                     'RC_OF_Sem_Contexto_TFI',
                     'RC_OF_Sem_Contexto_Licença',
                     'RC_OF_Sem_Contexto_Exclusão',
                     'RD Checklist Licenciamento',
                     'RD Checklist Licenciamento',
                     'RD_CheckList_Alt_Téc_FM',
                     'RD_CheckList_Alt_Téc_FM',
                     'RD_CheckList_Alt_Téc_OM',
                     'RD_CheckList_Alt_Téc_OM',
                     'RD_CheckList_Alt_Téc_TV-RTV',
                     'RD_CheckList_Alt_Téc_TV-RTV',
                     'RD_CheckList_Alt_Téc_TVD-RTVD',
                     'RD_CheckList_Alt_Téc_TVD-RTVD',
                     'RD_Checklist_Documentação',
                     'RD_Checklist_Documentação',
                     'RD_Despacho_Decisório_alterações',
                     'RD_Despacho_Decisório_alterações',
                     'RD_e-mail_Aprovação_de_Projeto_no_Mosaico',
                     'RD_e-mail_Aprovação_de_Projeto_no_Mosaico',
                     'RD_e-mail_Libera_Autocadastramento_no_Mosaico',
                     'RD_e-mail_Libera_Autocadastramento_no_Mosaico',
                     'RD_Email_Despacho-Alteracao_Tecnica',
                     'RD_Email_Despacho-Alteracao_Tecnica',
                     'RD_Email_Informa_Processo-Concluido_Autocad',
                     'RD_Email_Informa_Processo-Concluido_Autocad',
                     'RD_Email_Situacao_AR-Devolvido',
                     'RD_Email_Situacao_AR-Devolvido',
                     'RD_Memo Redução ERP PB.',
                     'RD_Memo Redução ERP PB.',
                     'RD_Memo_Ato_RF',
                     'RD_Memo_Ato_RF',
                     'RD_Memo_AUTOCADASTRAMENTO',
                     'RD_Memo_AUTOCADASTRAMENTO',
                     'RD_Memo_Retransm_Aux_Digital',
                     'RD_Memo_Retransm_Aux_Digital',
                     'RD_Of_Autocad_Processo_Unico',
                     'RD_Of_Autocad_Processo_Unico',
                     'RD_Of_Autocad_Varios_Processos',
                     'RD_Of_Autocad_Varios_Processos',
                     'RD_Of_Despacho_Decisorio',
                     'RD_Of_Despacho_Decisorio',
                     'RD_Of_Despacho_TFI',
                     'RD_Of_Despacho_TFI',
                     'RD_Of_ERAD',
                     'RD_Of_ERAD',
                     'RD_Of_Exigência',
                     'RD_Of_Exigência',
                     'RD_Of_Exigência_2',
                     'RD_Of_Exigência_2',
                     'RD_Of_Exigência_Alt_Tec_Mosaico',
                     'RD_Of_Exigência_Alt_Tec_Mosaico',
                     'RD_Of_Exigência_MC_ORLE',
                     'RD_Of_Exigência_MC_ORLE',
                     'RD_Of_Exig_Autocad_Ato_RF',
                     'RD_Of_Exig_Autocad_Ato_RF',
                     'RD_Of_Exig_Libera_Autocad',
                     'RD_Of_Exig_Libera_Autocad',
                     'RD_Of_Exig_Proj_Aba_Solicitações',
                     'RD_Of_Exig_Proj_Aba_Solicitações',
                     'RD_Of_Informa_AC_Liberado_Proc_Único',
                     'RD_Of_Informa_AC_Liberado_Proc_Único',
                     'RD_Of_Informa_AC_Liberado_Vários_Procs',
                     'RD_Of_Informa_AC_Liberado_Vários_Procs',
                     'RD_Of_Informa_Autocad_Customizado',
                     'RD_Of_Informa_Autocad_Customizado',
                     'RD_Of_Informa_Licenciamento_via_Mosaico',
                     'RD_Of_Informa_Licenciamento_via_Mosaico',
                     'RD_Of_Licença',
                     'RD_Of_Licença',
                     'RD_Of_MCTIC',
                     'RD_Of_MCTIC',
                     'RD_Of_MCTIC_Devolve_canal_adaptacao_OM_FM',
                     'RD_Of_MCTIC_Devolve_canal_adaptacao_OM_FM',
                     'RD_Of_MCTIC_Envio_de_Processo_a_pedido',
                     'RD_Of_MCTIC_Envio_de_Processo_a_pedido',
                     'RD_Of_MCTIC_RADCOM',
                     'RD_Of_MCTIC_RADCOM',
                     'RD_Of_Não_Outorgadas',
                     'RD_Of_Não_Outorgadas',
                     'RD_Of_pedido_e_eng_liberado',
                     'RD_Of_pedido_e_eng_liberado',
                     'RD_Of_Renovação_Entidade_Liberada',
                     'RD_Of_Renovação_Entidade_Liberada',
                     'RD_Of_Renovação_MCTIC',
                     'RD_Of_Renovação_MCTIC',
                     'SARC/SLP_Despacho Ordinatório de Arquivamento',
                     'SARC/SLP_Despacho Ordinatório de Arquivamento',
                     'SARC/SLP_Memorando Fiscalização_Com Autorização',
                     'SARC/SLP_Memorando Fiscalização_Com Autorização',
                     'SARC/SLP_Memorando Fiscalização_Sem Autorização',
                     'SARC/SLP_Memorando Fiscalização_Sem Autorização',
                     'SARC_Ato Revogação_Com Fiscalização',
                     'SARC_Ato Revogação_Com Fiscalização',
                     'SARC_Ato Revogação_Sem Fiscalização',
                     'SARC_Ato Revogação_Sem Fiscalização',
                     'SARC_Indeferimento',
                     'SARC_Indeferimento',
                     'SARC_Reiteração',
                     'SARC_Reiteração',
                     'SLMM/SLMA - Autocadastramento - Razão Social (CNPJ',
                     'SLMM/SLMA - Autocadastramento - Razão Social (CNPJ',
                     'SLP _ Check List de Análise',
                     'SLP _ Check List de Análise',
                     'SLP_Ato Revogaçãop_Com Fiscalização',
                     'SLP_Ato Revogaçãop_Com Fiscalização',
                     'SLP_Ato Revogação_Cassação.',
                     'SLP_Ato Revogação_Cassação.',
                     'SLP_Ato Revogação_Sem Fiscalização',
                     'SLP_Ato Revogação_Sem Fiscalização',
                     'SLP_Exigência_Documentação Complementar',
                     'SLP_Exigência_Documentação Complementar',
                     'SLP_Indeferimento',
                     'SLP_Indeferimento',
                     'SLP_Indeferimento Autocadastramento_corresp. elet.',
                     'SLP_Indeferimento Autocadastramento_corresp. elet.',
                     'SLP_Indeferimento Prorrogação',
                     'SLP_Indeferimento Prorrogação',
                     'SLP_Informe_Exclusão Serviço',
                     'SLP_Informe_Exclusão Serviço',
                     'SLP_Ofício Cancelamento Autorização_Com Débito',
                     'SLP_Ofício Cancelamento Autorização_Com Débito',
                     'SLP_Ofício Cancelamento Autorização_Sem Débito',
                     'SLP_Ofício Cancelamento Autorização_Sem Débito',
                     'Termo de Desanexação',
                     'Termo de Desanexação',
                     'Todas variáveis',
                     'Todas variáveis',
                     'vaznetto_RD_Of_Informa_Autocad',
                     'vaznetto_RD_Of_Informa_Autocad']

    HIPOTESES = [' ',
                'Controle Interno (Art. 26, § 3º, da Lei nº 10.180/2001)',
                'Controle Interno (Art. 26, § 3º, da Lei nº 10.180/2001)',
                'Direito Autoral (Art. 24, III, da Lei nº 9.610/1998)',
                'Direito Autoral (Art. 24, III, da Lei nº 9.610/1998)',
                'Documento Preparatório (Art. 7º, § 3º, da Lei nº 12.527/2011)',
                'Documento Preparatório (Art. 7º, § 3º, da Lei nº 12.527/2011)',
                'Fiscalização / Investigação da Anatel (Art. 174 da Lei nº 9.472/1997)',
                'Fiscalização / Investigação da Anatel (Art. 174 da Lei nº 9.472/1997)',
                'Informação Pessoal (Art. 31 da Lei nº 12.527/2011)',
                'Informação Pessoal (Art. 31 da Lei nº 12.527/2011)',
                'Informações Contábeis de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Contábeis de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Econômico-Financeiras de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Econômico-Financeiras de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Operacionais de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Operacionais de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Privilegiadas de Sociedades Anônimas (Art. 155, § 2º, da Lei nº 6.404/1976)',
                'Informações Privilegiadas de Sociedades Anônimas (Art. 155, § 2º, da Lei nº 6.404/1976)',
                'Informações Técnicas de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Informações Técnicas de Empresa (Art. 39, parágrafo único, da Lei nº 9.472/1997)',
                'Interceptação de Comunicações Telefônicas (Art. 8º, caput, da Lei nº 9.296/1996)',
                'Interceptação de Comunicações Telefônicas (Art. 8º, caput, da Lei nº 9.296/1996)',
                'Investigação de Responsabilidade de Servidor (Art. 150 da Lei nº 8.112/1990)',
                'Investigação de Responsabilidade de Servidor (Art. 150 da Lei nº 8.112/1990)',
                'Livros e Registros Contábeis Empresariais (Art. 1.190 do Código Civil)',
                'Livros e Registros Contábeis Empresariais (Art. 1.190 do Código Civil)',
                'Operações Bancárias (Art. 1º da Lei Complementar nº 105/2001)',
                'Operações Bancárias (Art. 1º da Lei Complementar nº 105/2001)',
                'Proteção da Propriedade Intelectual de Software (Art. 2º da Lei nº 9.609/1998)',
                'Proteção da Propriedade Intelectual de Software (Art. 2º da Lei nº 9.609/1998)',
                'Protocolo -Pendente Análise de Restrição de Acesso (Art. 6º, III, da Lei nº 12.527/2011)',
                'Protocolo -Pendente Análise de Restrição de Acesso (Art. 6º, III, da Lei nº 12.527/2011)',
                'Segredo de Justiça no Processo Civil (Art. 189 do Código de Processo Civil)',
                'Segredo de Justiça no Processo Civil (Art. 189 do Código de Processo Civil)',
                'Segredo de Justiça no Processo Penal (Art. 201, § 6º, do Código de Processo Penal)',
                'Segredo de Justiça no Processo Penal (Art. 201, § 6º, do Código de Processo Penal)',
                'Segredo Industrial (Art. 195, XIV, Lei nº 9.279/1996)',
                'Segredo Industrial (Art. 195, XIV, Lei nº 9.279/1996)',
                'Sigilo das Comunicações (Art. 3º, V, da Lei nº 9.472/1997)',
                'Sigilo das Comunicações (Art. 3º, V, da Lei nº 9.472/1997)',
                'Sigilo de Empresa em Situação Falimentar (Art. 169 da Lei nº 11.101/2005)',
                'Sigilo de Empresa em Situação Falimentar (Art. 169 da Lei nº 11.101/2005)',
                'Sigilo do Inquérito Policial (Art. 20 do Código de Processo Penal)',
                'Sigilo do Inquérito Policial (Art. 20 do Código de Processo Penal)',
                'Situação Econômico-Financeira de Sujeito Passivo (Art. 198, caput, da Lei nº 5.172/1966 - CTN)',
                'Situação Econômico-Financeira de Sujeito Passivo (Art. 198, caput, da Lei nº 5.172/1966 - CTN)']

class Externo(object):

    tipo = (By.ID, )

class Pesq_contato(object):

    ID_SEARCH = (By.ID, "txtPalavrasPesquisaContatos")

    TITLE = "SEI - Contatos"

class Contato(object):

    TITLE = 'SEI - Contatos'

    BTN_NOVO = (By.ID, 'btnNovo')

    BTN_PESQUISAR = (By.ID, "btnPesquisar")

    TIPO = (By.ID, 'selTipoContato')

    SIGLA = (By.ID, 'txtSigla')

    PF = (By.ID, 'lblPessoaFisica')

    NOME = (By.ID, 'txtNome')

    END = (By.ID, 'txtEndereco')

    COMP = (By.ID, 'txtComplemento')

    BAIRRO = (By.ID, 'txtBairro')

    PAIS = (By.ID, "selPais")

    UF = (By.ID, 'selUf')

    CIDADE = (By.ID, 'selCidade')

    CEP = (By.ID, 'txtCep')

    MASCULINO = (By.ID, 'optFeminino')

    FEMININO = (By.ID, 'optMasculino')

    CPF = (By.ID, 'txtCpf')

    RG = (By.ID, 'txtRg')

    ORG = (By.ID, 'txtOrgaoExpedidor')

    NASC = (By.ID, 'txtNascimento')

    FONE = (By.ID, 'txtTelefoneFixoPF')

    CEL = (By.ID, 'txtTelefoneCelularPF')

    EMAIL = (By.ID, 'txtEmail')

    SALVAR = (By.NAME, 'sbmAlterarContato')

    SALVAR_NOVO = (By.NAME, 'sbmCadastrarContato')

    OBS = (By.ID, 'txtaObservacao')

class Boleto(object):

    imprimir = dict(link='http://sistemasnet/boleto/Boleto/ConsultaDebitos.asp',
                    id_fistel=(By.ID, 'indTipoConsulta0'),
                    id_cpf=(By.ID, 'indTipoConsulta1'),
                    input_fistel=(By.ID, 'NumFistel'),
                    input_cpf=(By.ID, 'NumCNPJCPF'),
                    input_data=(By.ID, 'DataPPDUR'),
                    submit=(By.ID, 'botaoFlatConfirmar'),
                    marcar_todos=(By.ID, 'botaoFlatMarcarTodos'),
                    btn_print=(By.ID, 'botaoFlatImprimirSelecionados'))

class Sec(object):

    Base = 'http://sistemasnet/SEC/'

    Consulta = 'http://sistemasnet/SEC/Tela.asp?SISQSmodulo=9336'

    Histor = 'http://sistemasnet/SEC/Chamada/Historico.asp?SISQSmodulo=11380'

    Agenda = 'http://sistemasnet/SEC/Default.asp?SISQSmodulo=7146&SISQSsistema=435'

    Agenda_Alt = 'http://sistemasnet/SEC/Agenda/Tela.asp?OP=a&SISQSmodulo=5817'

    Agenda_Canc = 'http://sistemasnet/SEC/Agenda/Tela.asp?OP=e&SISQSmodulo=5818'

    Agenda_Cons = 'http://sistemasnet/SEC/Agenda/Tela.asp?OP=c&SISQSmodulo=5819'

    Agenda_Incl = 'http://sistemasnet/SEC/Agenda/Tela.asp?OP=i&Acao=i&SISQSmodulo=5813'

    Agenda_TrAval = 'http://sistemasnet/SEC/Morse/AvaliadorAlterar/tela.asp?SISQSmodulo=7851'

    Cert_Alt = 'http://sistemasnet/SEC/Certificado/alterar/tela.asp?SISQSmodulo=12486'

    Cert_Ant = 'http://sistemasnet/SEC/Certificado/Anterior/Tela.asp?SISQSmodulo=10530'

    Cert_Cert = 'http://sistemasnet/SEC/Certificado/Certificar/Tela.asp?SISQSmodulo=4063'

    Cert_Estr_Incl = 'http://sistemasnet/SEC/Certificado/Estrangeiro/Incluir/Tela.asp?SISQSmodulo=11713'

    Cert_Estr_Prorr = 'http://sistemasnet/SEC/Certificado/Estrangeiro/Prorrogar/Tela.asp?SISQSmodulo=11488'

    Cert_Excl = 'http://sistemasnet/SEC/Certificado/Exclusao/Tela.asp?SISQSmodulo=8100'

    Cert_Impr = 'http://sistemasnet/SEC/Certificado/Imprimir/Tela.asp?SISQSmodulo=8370'

    Cert_Mnt = 'http://sistemasnet/SEC/Certificado/Manutencao/Tela.asp?xOp=2&SISQSmodulo=10619'

    Cert_Reat = 'http://sistemasnet/SEC/Certificado/Reativar/Tela.asp?SISQSmodulo=19806'

    Cert_2nVia = 'http://sistemasnet/SEC/Certificado/SegundaVia/Tela.asp?SISQSmodulo=4145'

    Ent_Alt = 'http://sistemasnet/SEC/Chamada/Entidade.asp?OP=A&SISQSmodulo=5263'

    Ent_AltRF = 'http://sistemasnet/SEC/Chamada/CadastroSRFRegularizado.asp?SISQSmodulo=16374'

    Ent_Incl = 'http://sistemasnet/SEC/Chamada/Entidade.asp?OP=I&SISQSmodulo=4150'

    Insc_Canc = 'http://sistemasnet/SEC/Inscricao/Cancelar/Tela.asp?SISQSmodulo=17306'

    Insc_Cons = 'http://sistemasnet/SEC/Consulta/Provamarcada/Tela.asp?SISQSmodulo=4090'

    Insc_Inc = 'http://sistemasnet/SEC/Inscricao/Incluir/Tela.asp?SISQSmodulo=4029'

    Insc_Mnt = 'http://sistemasnet/SEC/Inscricao/Reativar/Tela.asp?SISQSmodulo=18333'

    Prova = namedtuple('Banca_Especial', 'imprimir responder')\
        ({'link': 'http://sistemasnet/SEC/Prova/BancaEspecialImpressao/Tela.asp',
         'id_cpf': (By.ID, 'NumCnpjCpf'),
         'submit': (By.ID, 'botaoFlatConfirmar'),
         'alt_reg': "AlteraNumReg();",
         'num_reg': (By.NAME, 'NumReg'),
         'id_bt_imprimir': (By.ID, "botaoFlat  Imprimir")},
         {}
        )

    Prova_Res = 'http://sistemasnet/SEC/Prova/Resultado/Tela.asp?SISQSmodulo=3872'

    submit = "submeterTela('http://sistemasnet/SEC/Chamada/Entidade.asp?SISQSModulo=&OP=A')"

class Agenda(object):

    data = (By.ID, "DataAgenda")

    hora = (By.ID, "HoraInicial")

    avaliador = (By.ID, "NumCpfAvaliador")

    local = (By.ID, "TxtLocalProva")

    ddd = (By.ID, "NumCodigoNacional")

    fone = (By.ID, "NumTelefone")

    responsavel = (By.ID, "NomeResponsavel")

    vagas = (By.ID, "NumVagas")

    morse = (By.ID, "IndMorse1")

    pc = (By.ID, "IndProvaAnatel1")

    dias = (By.ID, "NumDiasFimInscricao")

    btn_endereco = (By.ID, "botaoFlatEndereço")

    cep = (By.ID, "CodCep1")

    btn_buscar_end = (By.ID, "buscarEndereco")

    numero = (By.ID, "EndNumero1")

    btn_certificado = (By.ID, "botaoFlatCertificado")

    select_cert_1 = (By.ID, "pc_cmbCodCertificado000")

    select_cert_2 = (By.ID, "pc_cmbCodCertificado001")

    btn_confirmar = (By.ID, "botaoFlatConfirmar")

Entidade = {'cpf': [(By.ID, 'pNumCnpjCpf'), (By.ID, 'pnumCPFCNPJ'), (By.ID, 'NumCNPJCPF')],
            'cnpj': [(By.ID, 'pNumCnpjCpf'), (By.ID, 'pnumCPFCNPJ')],
            'fistel': [(By.ID, 'pNumFistel'), (By.ID, 'pnumFistel')], 'indicativo': [(By.ID, 'pIndicativo')],
            'nome': (By.ID, 't_NomeEntidade'), 'email': (By.ID, 't_EndEletronico'), 'rg': (By.ID, 'pf_NumIdentidade'),
            'orgexp': (By.ID, 'pf_SiglaOrgaoExp'), 'nasc': (By.ID, 'pf_DataNascimento'),
            'ddd': (By.ID, 'tel_NumCodigoNacional0'), 'fone': (By.ID, 'tel_NumTelefone0'), 'cep': (By.ID, 'CodCep1'),
            'bt_cep': (By.ID, 'buscarEndereco'), 'logr': (By.ID, 'EndLogradouro1'), 'num': (By.ID, 'EndNumero1'),
            'comp': (By.ID, 'EndComplemento1'), 'bairro': (By.ID, 'EndBairro1'), 'uf': (By.ID, 'SiglaUf1'),
            'cidade': (By.ID, 'CodMunicipio1'), 'confirmar': (By.ID, 'botaoFlatConfirmar'),
            'bt_dados': (By.ID, 'botaoFlatDadosComplementares'), 'bt_fone': (By.ID, 'botaoFlatTelefones'),
            'bt_end': (By.ID, 'botaoFlatEndereço')}

class Scpx(object):


    IDS = dict(cpf=((By.ID, 'pNumCnpjCpf'), (By.ID, 'NumCNPJCPF'), (By.ID, 'pnumCPFCNPJ')),
               fistel=((By.ID, 'pNumFistel'), (By.ID, 'pnumFistel')),
               indicativo=((By.ID, 'pIndicativo'),))

    submit = ((By.ID, "botaoFlatConfirmar"),)

    consulta = {'link': 'http://sistemasnet/scpx/Consulta/Tela.asp?SISQSmodulo=12714',
                'id_nome': (By.ID, 'pNomeEntidade'),
                'id_cpf': (By.ID, 'pNumCnpjCpf'),
                'id_fistel': (By.ID, 'pNumFistel'),
                'id_indicativo': (By.ID, 'pIndicativo'),
                'id_btn_estacao': (By.ID, "botaoFlatEstação"),
                'submit': (By.ID, "botaoFlatConfirmar"),
                'impressao_completa': (By.ID, 'botaoFlatVersãoparaImpressão'),
                'impressao_resumida': (By.ID, 'botaoFlatVersãoResumida'),
                'imprimir': (By.ID, 'botaoFlatCLIQUEAQUIPARAIMPRIMIR'),
                'frame_impressao': 'imprime1'}

    historico = {'link': 'http://sistemasnet/scpx/Chamada/Historico.asp?SISQSmodulo=12731',
                 'id_cpf': (By.ID, 'pNumCnpjCpf'),
                 'id_fistel': (By.ID, 'pNumFistel'),
                 'id_indicativo': (By.ID, 'pIndicativo'),
                 'submit': consulta['submit']}

    entidade_alterar = {'link': "http://sistemasnet/scpx/Chamada/CadastroSRFRegularizado.asp",
                        'id_cpf': (By.ID, 'NumCNPJCPF'),
                        'submit': (By.ID, 'botaoFlatConfirmar')}

    entidade_incluir = {'incluir': "http://sistemasnet/scpx/Chamada/Entidade.asp?OP=I",
                        'id_cpf': (By.ID, 'pNumCnpjCpf')}

    estacao = {'incluir': "http://sistemasnet/scpx/Estacao/Tela.asp?OP=I",
               'alterar': "http://sistemasnet/scpx/Estacao/Tela.asp?OP=A",
               'excluir': "http://sistemasnet/scpx/Estacao/Tela.asp?OP=E",
               'licenciar': "http://sistemasnet/scpx/EstacaoLicenciar/Tela.asp",
               'id_cpf': (By.ID, 'pNumCnpjCpf'),
               'id_fistel': (By.ID, 'pNumFistel'),
               'id_btn_dados_estacao': (By.ID, "botaoFlatDadosdaEstação"),
               'id_btn_lista_estacoes': (By.ID, "botaoFlatListadeEstações"),
               'id_btn_licenciar': (By.ID, "botaoFlatLicenciar"),
               'id_uf': (By.ID, "cmbUF"),
               'id_indicativo': (By.ID, "NomeIndicativo"),
               'id_seq': (By.ID, "NumSequenciaIndicativo"),
               'id_tipo': (By.ID, "cmbTipoEstacao"),
               'copiar_sede': (By.ID, "botaoFlatCopiarEndereçoSede"),
               'submit': (By.ID, "botaoFlatConfirmar")}

    formulario_imprimir = {'link': 'http://sistemasnet/scpx/Formulario/Tela.asp',
                           'id_cpf': (By.ID, 'pNumCnpjCpf'),
                           'id_fistel': (By.ID, 'pNumFistel'),
                           'id_indicativo': (By.ID, 'pIndicativo'),
                           'submit': (By.ID, 'botaoFlatConfirmar')}

    movimento = {'transferir': "http://sistemasnet/scpx/MovimentoTransferir/Tela.asp",
                 'cancelar': 'http://sistemasnet/scpx/MovimentoCancelar/Tela.asp',
                 'id_btn_lista_estacoes': estacao['id_btn_lista_estacoes'],
                 'id_btn_marcar_todos': (By.ID, 'botaoFlatMarcarTodos'),
                 'id_txt_cancelar': (By.ID, 'TxtComentarioMov'),
                 'id_cpf': consulta['id_cpf'],
                 'id_proc': (By.ID, 'NumProcesso'),
                 'submit': (By.ID, "botaoFlatConfirmar"),
                 'id_atual': (By.ID, "pMovimento"),
                 'id_posterior': (By.ID, "CodTipoMovimento")}

    liberar_indicativo = {'link': 'http://sistemasnet/scpx/IndicativoLiberar/Tela.asp',
                          'id_uf': (By.ID, 'SiglaUF'),
                          'id_indicato': (By.ID, 'Indicativo'),
                          'id_sequencial': (By.ID, 'Sequencial'),
                          'submit': (By.ID, 'botaoFlatConfirmar')}

    licenca_imprimir = {'link': 'http://sistemasnet/scpx/Licenca/Tela.asp',
               }

    servico = {'incluir': "http://sistemasnet/scpx/Servico/Tela.asp?Op=I",
               'prorrogar_rf': "http://sistemasnet/scpx/ServicoProrrogar/Tela.asp",
               'excluir': 'http://sistemasnet/scpx/Servico/Tela.asp?Op=E',
               'id_num_proc': (By.ID, 'NumProcesso'),
               'id_cpf': (By.ID, 'pNumCnpjCpf'),
               'id_btn_dados_estacao': (By.ID, "botaoFlatEstação"),
               'id_btn_dados_exclusão': (By.ID, 'botaoFlatDadosExclusão'),
               'id_btn_corresp': (By.ID, 'botaoFlatEndereçoCorrespondência'),
               'id_doc_exclusão': (By.ID, 'pDocAto'),
               'id_motivo_exclusão': (By.ID, "CodMotivoExclusao"),
               'submit': (By.ID, "botaoFlatConfirmar")}

    licenca = {'imprimir': {'link': "http://sistemasnet/scpx/Licenca/Tela.asp",
                            'id_cpf': (By.ID, 'pnumCPFCNPJ'),
                            'submit': estacao['submit'],
                            'id_btn_imprimir': (By.ID, 'botaoFlatImprimir')},
               'prorrogar': "http://sistemasnet/scpx/LicencaProrrogar/Tela.asp",
               '2_via': 'http://sistemasnet/scpx/Licenca2Via/Tela.asp',
               'id_cpf': (By.ID, 'pnumCPFCNPJ'),
               'id_fistel': (By.ID, 'pnumFistel'),
               'id_indicativo': Entidade['indicativo'],
               'id_btn_lista_estacoes': estacao['id_btn_lista_estacoes'],
               'submit': estacao['submit']}

    licenca_prorrogar = {"link": "http://sistemasnet/scpx/LicencaProrrogar/Tela.asp",
                         "id_cpf": (By.ID, 'pNumCnpjCpf'),
                         'id_fistel': (By.ID, 'pnumFistel'),
                         'id_indicativo': Entidade['indicativo'],
                         'id_btn_lista_estacoes': estacao['id_btn_lista_estacoes'],
                         'submit': estacao['submit']}

class Scra(object):

    Consulta = dict(link='http://sistemasnet/SCRA/Consulta/Tela.asp')

    Ent =      dict(alterar_situacao="http://sistemasnet/scra/Chamada/CadastroSRFRegularizado.asp",
                    incluir="http://sistemasnet/scpx/Chamada/Entidade.asp?OP=I")

    Estacao =  dict(alterar="http://sistemasnet/acra/Chamada/Entidade.asp?OP=A",
                    alterar_indicativo='http://sistemasnet/SCRA/IndicativoAlterar/Tela.asp?OP=A',
                    excluir="http://sistemasnet/SCRA/Estacao/Tela.asp?OP=E",
                    incluir='http://sistemasnet/SCRA/Estacao/Tela.asp?OP=I',
                    licenciar='http://sistemasnet/SCRA/EstacaoLicenciar/Tela.asp')

    Licenca =  dict(imprimir="http://sistemasnet/SCRA/Chamada/Licenca.asp")

class Slmm(object):

    Consulta = 'http://sistemasnet/stel/SCMM/Consulta/Tela.asp'

    Licenca = {"imprimir": "http://sistemasnet/stel/SCMM/LicencaImprimir/Tela.asp?SISQSmodulo=7766"}

class Slma(object):

    Consulta = "http://sistemasnet/stel/SCMA/Consulta/Tela.asp"


    Licenca = {"imprimir": "http://sistemasnet/stel/SCMA/LicencaPadrao/ImpressaoLicenca.asp?SISQSmodulo=7005"}

class Sigec(object):

    consulta = {'geral': {'link': "http://sistemasnet/sigec/ConsultasGerais/SituacaoCadastral/tela.asp",
                          'id_cpf': (By.ID, "NumCNPJCPF"),
                          'id_fistel': (By.ID, "NumFistel"),
                          'id_indicativo': (By.ID, "NomeIndicativo"),
                          'id_nome': (By.ID, "NomeEntidade"),
                          'id_btn_exata': (By.ID, "indTipoComparacao0"),
                          'id_btn_init': (By.ID, "indTipoComparacao1")}
                }




    cpf = (By.ID, "NumCNPJCPF")

    fistel = (By.ID, 'NumFistel')

    Consulta = {'id_confirmar': (By.ID, 'botaoFlatConfirmar')}








