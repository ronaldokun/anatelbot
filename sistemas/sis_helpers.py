#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:59 2017

@author: ronaldo
"""

from collections import namedtuple

from selenium.webdriver.common.by import By

SISTEMASNET = "http://sistemasnet/"



class Sapiens(object):
    URL = "https://sapiens.agu.gov.br/"

    TITLE = "SAPIENS"

    LOGIN = (By.ID, "cpffield-1017-inputEl")

    SENHA = (By.ID, "textfield-1018-inputEl")


class Rf_Sapiens(object):

    URL = "https://sapiens.agu.gov.br/receitafederal"

    BTN_PF = (By.ID, "tab-1083-btnInnerE1")

    BTN_PJ = (By.ID, "tab-1084-btnInnerEl")

    ID_INPUT_CPF = (By.ID, "textfield-1014-inputEl")

    ID_INPUT_CNPJ = (By.ID, "textfield-1051-inputEl")

    RESULTADO = (By.CLASS_NAME, "x-grid-cell-inner")

    CPF = (By.ID, "textfield-1014-inputEl")

    NAME = (By.ID, "textfield-1015-inputE1")


class Boleto(object):

    imprimir = dict(
        link="http://sistemasnet/boleto/Boleto/ConsultaDebitos.asp",
        id_fistel=(By.ID, "indTipoConsulta0"),
        id_cpf=(By.ID, "indTipoConsulta1"),
        input_fistel=(By.ID, "NumFistel"),
        input_cpf=(By.ID, "NumCNPJCPF"),
        input_data=(By.ID, "DataPPDUR"),
        submit=(By.ID, "botaoFlatConfirmar"),
        marcar_todos=(By.ID, "botaoFlatMarcarTodos"),
        btn_print=(By.ID, "botaoFlatImprimirSelecionados"),
    )


class Sec(object):

    Base = "http://sistemasnet/SEC/"

    consulta = {
        "link": "http://sistemasnet/SEC/ConsultaDocumentos/Tela.asp",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pNumFistel"),
        "id_nome": (By.ID, "pNomeEntidade"),
        "id_btn_exata": (By.ID, "pindTipoComparacao0"),
        "id_btn_init": (By.ID, "pindTipoComparacao1"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    Histor = "http://sistemasnet/SEC/Chamada/Historico.asp?SISQSmodulo=11380"

    Agenda = "http://sistemasnet/SEC/Default.asp?SISQSmodulo=7146&SISQSsistema=435"

    Agenda_Alt = "http://sistemasnet/SEC/Agenda/Tela.asp?OP=a&SISQSmodulo=5817"

    Agenda_Canc = "http://sistemasnet/SEC/Agenda/Tela.asp?OP=e&SISQSmodulo=5818"

    Agenda_Cons = "http://sistemasnet/SEC/Agenda/Tela.asp?OP=c&SISQSmodulo=5819"

    Agenda_Incl = "http://sistemasnet/SEC/Agenda/Tela.asp?OP=i&Acao=i&SISQSmodulo=5813"

    Agenda_TrAval = (
        "http://sistemasnet/SEC/Morse/AvaliadorAlterar/tela.asp?SISQSmodulo=7851"
    )

    Cert_Alt = "http://sistemasnet/SEC/Certificado/alterar/tela.asp?SISQSmodulo=12486"

    Cert_Ant = "http://sistemasnet/SEC/Certificado/Anterior/Tela.asp?SISQSmodulo=10530"

    Cert_Cert = (
        "http://sistemasnet/SEC/Certificado/Certificar/Tela.asp?SISQSmodulo=4063"
    )

    Cert_Estr_Incl = "http://sistemasnet/SEC/Certificado/Estrangeiro/Incluir/Tela.asp?SISQSmodulo=11713"

    Cert_Estr_Prorr = "http://sistemasnet/SEC/Certificado/Estrangeiro/Prorrogar/Tela.asp?SISQSmodulo=11488"

    Cert_Excl = "http://sistemasnet/SEC/Certificado/Exclusao/Tela.asp?SISQSmodulo=8100"

    Cert_Impr = "http://sistemasnet/SEC/Certificado/Imprimir/Tela.asp?SISQSmodulo=8370"

    Cert_Mnt = (
        "http://sistemasnet/SEC/Certificado/Manutencao/Tela.asp?xOp=2&SISQSmodulo=10619"
    )

    Cert_Reat = "http://sistemasnet/SEC/Certificado/Reativar/Tela.asp?SISQSmodulo=19806"

    Cert_2nVia = (
        "http://sistemasnet/SEC/Certificado/SegundaVia/Tela.asp?SISQSmodulo=4145"
    )

    entidade = {
        "alterar": {
            "link": "http://sistemasnet/SEC/Chamada/Entidade.asp?OP=A",
            "id_cpf": (By.ID, "pNumCnpjCpf"),
            "id_resp": (By.ID, "pf_NumCpfResponsavel"),
            "id_nome": (By.ID, "pNomeEntidade"),
            "input_nome": (By.ID, "t_NomeEntidade"),
            "E-mail": (By.ID, "t_EndEletronico"),
            "CNPJ/CPF_Responsável": (By.ID, "pf_NumCpfResponsavel"),
            "bt_alt_razao": (By.ID, "alteraRazao"),
            "id_novo_nome": (By.ID, "t_nNomeEntidade"),
            "id_p_altera": (By.ID, "t_NumProcessoAlteracaoNome"),
            "Identidade": (By.ID, "pf_NumIdentidade"),
            "Órgão Exp.": (By.ID, "pf_SiglaOrgaoExp"),
            "Data de Nascimento": (By.ID, "pf_DataNascimento"),
            "DDD": (By.ID, "tel_NumCodigoNacional0"),
            "Principal": (By.ID, "tel_NumTelefone0"),
            "DDD2": (By.ID, "tel_NumCodigoNacional1"),
            "Principal2": (By.ID, "tel_NumTelefone1"),
            "CEP": (By.ID, "CodCep1"),
            "bt_cep": (By.ID, "buscarEndereco"),
            "Logradouro": (By.ID, "EndLogradouro1"),
            "Número": (By.ID, "EndNumero1"),
            "Complemento": (By.ID, "EndComplemento1"),
            "Bairro": (By.ID, "EndBairro1"),
            "Cidade": (By.ID, "CodMunicipio1"),
            "UF": (By.ID, "SiglaUf1"),
            "bt_dados": (By.ID, "botaoFlatDadosComplementares"),
            "bt_fone": (By.ID, "botaoFlatTelefones"),
            "bt_end": (By.ID, "botaoFlatEndereço"),
            "submit_script": "submeterTela('http://sistemasnet/SEC/Chamada/Entidade.asp?SISQSModulo=&OP=A')",
            "submit": (By.ID, "botaoFlatConfirmar"),
            "atualizar_ok": "Operação realizada com Sucesso!",
        },
        "incluir": {
            "link": "http://sistemasnet/SEC/Chamada/Entidade.asp?OP=I",
            "alterar_nome": (By.ID, "alteraRazao"),
            "nome_novo": (By.ID, "t_nNomeEntidade"),
            "num_doc": (By.ID, "t_NumProcessoAlteracaoNome"),
            "id_cpf": (By.ID, "pNumCnpjCpf"),
            "id_nome": (By.ID, "pNomeEntidade"),
            "input_nome": (By.ID, "t_NomeEntidade"),
            "submit": (By.ID, "botaoFlatConfirmar"),
            "E-mail": (By.ID, "t_EndEletronico"),
            "CNPJ/CPF_Responsável": (By.ID, "pf_NumCpfResponsavel"),
            "Identidade": (By.ID, "pf_NumIdentidade"),
            "Órgão Exp.": (By.ID, "pf_SiglaOrgaoExp"),
            "Data de Nascimento": (By.ID, "pf_DataNascimento"),
            "DDD": (By.ID, "tel_NumCodigoNacional0"),
            "Principal": (By.ID, "tel_NumTelefone0"),
            "DDD2": (By.ID, "tel_NumCodigoNacional1"),
            "Principal2": (By.ID, "tel_NumTelefone1"),
            "CEP": (By.ID, "CodCep1"),
            "bt_cep": (By.ID, "buscarEndereco"),
            "Logradouro": (By.ID, "EndLogradouro1"),
            "Número": (By.ID, "EndNumero1"),
            "Complemento": (By.ID, "EndComplemento1"),
            "Bairro": (By.ID, "EndBairro1"),
            "Cidade": (By.ID, "CodMunicipio1"),
            "UF": (By.ID, "SiglaUf1"),
            "bt_dados": (By.ID, "botaoFlatDadosComplementares"),
            "bt_fone": (By.ID, "botaoFlatTelefones"),
            "bt_end": (By.ID, "botaoFlatEndereço"),
            "submit_script": "submeterTela('http://sistemasnet/SEC/Chamada/Entidade.asp?SISQSModulo=&OP=A')",
            "submit": (By.ID, "botaoFlatConfirmar"),
            "atualizar_ok": "Operação realizada com Sucesso!",
        },
        "regularizar_RF": {
            "link": "http://sistemasnet/SEC/Chamada/CadastroSRFRegularizado.asp",
            "id_cpf": (By.ID, "NumCNPJCPF"),
            "submit": (By.ID, "botaoFlatConfirmar"),
            "nova_situacao": (By.ID, "CodSituacaoCadastralNova"),
            "atualizar_ok": "Operação realizada com Sucesso!",
        },
    }

    inscricao = {
        "incluir": {
            "link": "http://sistemasnet/SEC/Inscricao/Incluir/Tela.asp",
            "id_cpf": (By.ID, "NumCnpjCpf"),
            "id_uf": (By.ID, "SiglaUF"),
            "id_certificado": (By.ID, "pCertCat"),
            "protocolo": (By.ID, "NumProtocolo"),
            "submit": (By.ID, "botaoFlatConfirmar"),
        },
        "consultar": {
            "link": "http://sistemasnet/SEC/Consulta/Provamarcada/Tela.asp",
            "id_cpf": (By.ID, "NumCnpjCpf"),
            "not_found": "Não foi encontrado o candidato.",
            "imprimir": (By.ID, "botaoFlatImprimir"),
        },
    }

    Ent_Incl = "http://sistemasnet/SEC/Chamada/Entidade.asp?OP=I&SISQSmodulo=4150"

    Insc_Canc = "http://sistemasnet/SEC/Inscricao/Cancelar/Tela.asp?SISQSmodulo=17306"

    Insc_Cons = "http://sistemasnet/SEC/Consulta/Provamarcada/Tela.asp?SISQSmodulo=4090"

    Insc_Mnt = "http://sistemasnet/SEC/Inscricao/Reativar/Tela.asp?SISQSmodulo=18333"

    Prova = {
        "imprimir": {
            "link": "http://sistemasnet/SEC/Prova/BancaEspecialImpressao/Tela.asp",
            "link_direto": r"http://sistemasnet/SEC/Prova/BancaEspecialImpressao/DadosProva.asp?idtProvaAgenda={0}&NumCpfAvaliador={1}",
            "id_cpf": (By.ID, "NumCnpjCpf"),
            "submit": (By.ID, "botaoFlatConfirmar"),
            "alt_reg": "AlteraNumReg();",
            "num_reg": (By.NAME, "NumReg"),
            "id_bt_imprimir": (By.ID, "botaoFlat  Imprimir"),
            "justificativa": (By.ID, "justificativa"),
        }
    }

    Prova_Res = "http://sistemasnet/SEC/Prova/Resultado/Tela.asp?SISQSmodulo=3872"


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


Entidade = {
    "cpf": [(By.ID, "pNumCnpjCpf"), (By.ID, "pnumCPFCNPJ"), (By.ID, "NumCNPJCPF")],
    "cnpj": [(By.ID, "pNumCnpjCpf"), (By.ID, "pnumCPFCNPJ")],
    "fistel": [(By.ID, "pNumFistel"), (By.ID, "pnumFistel")],
    "indicativo": [(By.ID, "pIndicativo")],
    "nome": (By.ID, "pNomeEntidade"),
    "email": (By.ID, "t_EndEletronico"),
    "rg": (By.ID, "pf_NumIdentidade"),
    "orgexp": (By.ID, "pf_SiglaOrgaoExp"),
    "nasc": (By.ID, "pf_DataNascimento"),
    "ddd": (By.ID, "tel_NumCodigoNacional0"),
    "fone": (By.ID, "tel_NumTelefone0"),
    "cep": (By.ID, "CodCep1"),
    "bt_cep": (By.ID, "buscarEndereco"),
    "logr": (By.ID, "EndLogradouro1"),
    "num": (By.ID, "EndNumero1"),
    "comp": (By.ID, "EndComplemento1"),
    "bairro": (By.ID, "EndBairro1"),
    "uf": (By.ID, "SiglaUf1"),
    "cidade": (By.ID, "CodMunicipio1"),
    "confirmar": (By.ID, "botaoFlatConfirmar"),
}


class Scpx(object):

    IDS = dict(
        cpf=((By.ID, "pNumCnpjCpf"), (By.ID, "NumCNPJCPF"), (By.ID, "pnumCPFCNPJ")),
        fistel=((By.ID, "pNumFistel"), (By.ID, "pnumFistel")),
        indicativo=((By.ID, "pIndicativo"),),
    )

    submit = (By.ID, "botaoFlatConfirmar")

    consulta = {
        "link": "http://sistemasnet/scpx/Consulta/Tela.asp?SISQSmodulo=12714",
        "id_nome": (By.ID, "pNomeEntidade"),
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pNumFistel"),
        "id_indicativo": (By.ID, "pIndicativo"),
        "id_btn_estacao": (By.ID, "botaoFlatEstação"),
        "submit": (By.ID, "botaoFlatConfirmar"),
        "impressao_completa": (By.ID, "botaoFlatVersãoparaImpressão"),
        "impressao_resumida": (By.ID, "botaoFlatVersãoResumida"),
        "imprimir": (By.ID, "botaoFlatCLIQUEAQUIPARAIMPRIMIR"),
        "frame_impressao": "imprime1",
    }

    historico = {
        "link": "http://sistemasnet/scpx/Chamada/Historico.asp?SISQSmodulo=12731",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pNumFistel"),
        "id_indicativo": (By.ID, "pIndicativo"),
        "submit": consulta["submit"],
    }

    entidade_alterar = {
        "link": "http://sistemasnet/scpx/Chamada/CadastroSRFRegularizado.asp",
        "id_cpf": (By.ID, "NumCNPJCPF"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    entidade_incluir = {
        "incluir": "http://sistemasnet/scpx/Chamada/Entidade.asp?OP=I",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
    }

    estacao = {
        "incluir": "http://sistemasnet/scpx/Estacao/Tela.asp?OP=I",
        "alterar": "http://sistemasnet/scpx/Estacao/Tela.asp?OP=A",
        "excluir": "http://sistemasnet/scpx/Estacao/Tela.asp?OP=E",
        "licenciar": "http://sistemasnet/scpx/EstacaoLicenciar/Tela.asp",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pNumFistel"),
        "id_btn_dados_estacao": (By.ID, "botaoFlatDadosdaEstação"),
        "id_btn_lista_estacoes": (By.ID, "botaoFlatListadeEstações"),
        "id_btn_licenciar": (By.ID, "botaoFlatLicenciar"),
        "id_uf": (By.ID, "cmbUF"),
        "id_indicativo": (By.ID, "NomeIndicativo"),
        "id_seq": (By.ID, "NumSequenciaIndicativo"),
        "id_tipo": (By.ID, "cmbTipoEstacao"),
        "copiar_sede": (By.ID, "botaoFlatCopiarEndereçoSede"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    formulario_imprimir = {
        "link": "http://sistemasnet/scpx/Formulario/Tela.asp",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pNumFistel"),
        "id_indicativo": (By.ID, "pIndicativo"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    movimento = {
        "transferir": "http://sistemasnet/scpx/MovimentoTransferir/Tela.asp",
        "cancelar": "http://sistemasnet/scpx/MovimentoCancelar/Tela.asp",
        "id_btn_lista_estacoes": estacao["id_btn_lista_estacoes"],
        "id_btn_marcar_todos": (By.ID, "botaoFlatMarcarTodos"),
        "id_txt_cancelar": (By.ID, "TxtComentarioMov"),
        "id_cpf": consulta["id_cpf"],
        "id_fistel": (By.ID, "pNumFistel"),
        "id_proc": (By.ID, "NumProcesso"),
        "submit": (By.ID, "botaoFlatConfirmar"),
        "id_atual": (By.ID, "pMovimento"),
        "id_posterior": (By.ID, "CodTipoMovimento"),
    }

    liberar_indicativo = {
        "link": "http://sistemasnet/scpx/IndicativoLiberar/Tela.asp",
        "id_uf": (By.ID, "SiglaUF"),
        "id_indicato": (By.ID, "Indicativo"),
        "id_sequencial": (By.ID, "Sequencial"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    licenca_imprimir = {"link": "http://sistemasnet/scpx/Licenca/Tela.asp"}

    servico = {
        "incluir": "http://sistemasnet/scpx/Servico/Tela.asp?Op=I",
        "prorrogar_rf": "http://sistemasnet/scpx/ServicoProrrogar/Tela.asp",
        "excluir": "http://sistemasnet/scpx/Servico/Tela.asp?Op=E",
        "id_num_proc": (By.ID, "NumProcesso"),
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_btn_dados_estacao": (By.ID, "botaoFlatEstação"),
        "id_btn_dados_exclusão": (By.ID, "botaoFlatDadosExclusão"),
        "id_btn_corresp": (By.ID, "botaoFlatEndereçoCorrespondência"),
        "id_doc_exclusão": (By.ID, "pDocAto"),
        "id_motivo_exclusão": (By.ID, "CodMotivoExclusao"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    licenca = {
        "imprimir": {
            "link": "http://sistemasnet/scpx/Licenca/Tela.asp",
            "id_cpf": (By.ID, "pnumCPFCNPJ"),
            "submit": estacao["submit"],
            "id_btn_imprimir": (By.ID, "botaoFlatImprimir"),
        },
        "prorrogar": "http://sistemasnet/scpx/LicencaProrrogar/Tela.asp",
        "2_via": "http://sistemasnet/scpx/Licenca2Via/Tela.asp",
        "id_cpf": (By.ID, "pnumCPFCNPJ"),
        "id_fistel": (By.ID, "pnumFistel"),
        "id_indicativo": Entidade["indicativo"],
        "id_btn_lista_estacoes": estacao["id_btn_lista_estacoes"],
        "submit": estacao["submit"],
    }

    licenca_prorrogar = {
        "link": "http://sistemasnet/scpx/LicencaProrrogar/Tela.asp",
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_fistel": (By.ID, "pnumFistel"),
        "id_indicativo": Entidade["indicativo"],
        "id_btn_lista_estacoes": estacao["id_btn_lista_estacoes"],
        "submit": estacao["submit"],
    }


class Scra(object):

    consulta = dict(
        link="http://sistemasnet/SCRA/Consulta/Tela.asp",
        id_nome=(By.ID, "pNomeEntidade"),
        id_cpf=(By.ID, "pNumCnpjCpf"),
        id_fistel=(By.ID, "pNumFistel"),
        id_indicativo=(By.ID, "pIndicativo"),
        id_btn_estacao=(By.ID, "botaoFlatEstação"),
        submit=(By.ID, "botaoFlatConfirmar"),
        impressao_completa=(By.ID, "botaoFlatVersãoparaImpressão"),
        impressao_resumida=(By.ID, "botaoFlatVersãoResumida"),
        imprimir=(By.ID, "botaoFlatCLIQUEAQUIPARAIMPRIMIR"),
        frame_impressao="imprime1",
    )

    Ent = dict(
        alterar_situacao="http://sistemasnet/scra/Chamada/CadastroSRFRegularizado.asp",
        incluir="http://sistemasnet/scpx/Chamada/Entidade.asp?OP=I",
    )

    estacao = dict(
        alterar="http://sistemasnet/scra/Chamada/Entidade.asp?OP=A",
        alterar_indicativo="http://sistemasnet/SCRA/IndicativoAlterar/Tela.asp?OP=A",
        excluir="http://sistemasnet/SCRA/Estacao/Tela.asp?OP=E",
        incluir="http://sistemasnet/SCRA/Estacao/Tela.asp?OP=I",
        licenciar="http://sistemasnet/SCRA/EstacaoLicenciar/Tela.asp",
        id_btn_lista_estacoes=(By.ID, "botaoFlatListadeEstações"),
    )

    servico = {
        "incluir": "http://sistemasnet/scra/Servico/Tela.asp?Op=I",
        "prorrogar_rf": "http://sistemasnet/scra/ServicoProrrogar/Tela.asp",
        "excluir": "http://sistemasnet/scra/Servico/Tela.asp?Op=E",
        "id_num_proc": (By.ID, "NumProcesso"),
        "id_cpf": (By.ID, "pNumCnpjCpf"),
        "id_btn_dados_estacao": (By.ID, "botaoFlatEstação"),
        "id_btn_dados_exclusão": (By.ID, "botaoFlatDadosExclusão"),
        "id_btn_corresp": (By.ID, "botaoFlatEndereçoCorrespondência"),
        "id_doc_exclusão": (By.ID, "pDocAto"),
        "id_motivo_exclusão": (By.ID, "CodMotivoExclusao"),
        "submit": (By.ID, "botaoFlatConfirmar"),
    }

    movimento = {
        "transferir": "http://sistemasnet/scra/MovimentoTransferir/Tela.asp",
        "cancelar": "http://sistemasnet/scra/MovimentoCancelar/Tela.asp",
        "id_btn_lista_estacoes": estacao["id_btn_lista_estacoes"],
        "id_btn_marcar_todos": (By.ID, "botaoFlatMarcarTodos"),
        "id_txt_cancelar": (By.ID, "TxtComentarioMov"),
        "id_cpf": consulta["id_cpf"],
        "id_proc": (By.ID, "NumProcesso"),
        "submit": (By.ID, "botaoFlatConfirmar"),
        "id_atual": (By.ID, "pMovimento"),
        "id_posterior": (By.ID, "CodTipoMovimento"),
    }

    licenca = {
        "imprimir": dict(
            link="http://sistemasnet/scra/Chamada/Licenca.asp",
            id_cpf=(By.ID, "pnumCPFCNPJ"),
            submit=(By.ID, "botaoFlatConfirmar"),
            id_btn_imprimir=(By.ID, "botaoFlatImprimirSelecionados"),
        )
    }


class Slmm(object):

    Consulta = "http://sistemasnet/stel/SCMM/Consulta/Tela.asp"

    Licenca = {
        "imprimir": "http://sistemasnet/stel/SCMM/LicencaImprimir/Tela.asp?SISQSmodulo=7766"
    }


class Slma(object):

    Consulta = "http://sistemasnet/stel/SCMA/Consulta/Tela.asp"

    Licenca = {
        "imprimir": "http://sistemasnet/stel/SCMA/LicencaPadrao/ImpressaoLicenca.asp?SISQSmodulo=7005"
    }


class Sigec(object):

    consulta = {
        "geral": {
            "link": "http://sistemasnet/sigec/ConsultasGerais/SituacaoCadastral/tela.asp",
            "id_cpf": (By.ID, "NumCNPJCPF"),
            "id_fistel": (By.ID, "NumFistel"),
            "id_indicativo": (By.ID, "NomeIndicativo"),
            "id_nome": (By.ID, "NomeEntidade"),
            "id_btn_exata": (By.ID, "indTipoComparacao0"),
            "id_btn_init": (By.ID, "indTipoComparacao1"),
        }
    }

    cpf = (By.ID, "NumCNPJCPF")

    fistel = (By.ID, "NumFistel")

    Consulta = {"id_confirmar": (By.ID, "botaoFlatConfirmar")}

