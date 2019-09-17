import os
import re
import sys
from collections import OrderedDict, namedtuple
from time import sleep
from typing import Dict, List

from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By

from tool import functions
from tool.page import *
from sistemas import sis_helpers

# This add the ../folder to the path while in development mode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Sistema(Page):
    def __init__(self, driver, login=None, senha=None, timeout:int=5):
        

        if login and senha:

            self.driver = functions.get_browser(driver, login, senha, timeout)

        else:

            self.driver = driver

    def _navigate(
        self, identificador: str, tipo_id: str, acoes: tuple, silent: bool = True, timeout:int=5
    ):
        """Check id and tipo_id consistency and navigate to link

        :param identificador, e.g. cpf: 11 digits, cnpj: 14 digits, indicativo: 4 to 6 characters
        :param tipo_id: cpf, cnpj or indicativo
        :param page_id: tuple (link to page, element id to fill, submit button)
        :return: None
        """
        identificador = functions.check_input(identificador=identificador, tipo=tipo_id)

        link, _id, submit = acoes

        self.driver.get(link)

        if silent:

            if submit is None:

                self._atualizar_elemento(_id, identificador + Keys.RETURN, timeout=timeout)

            else:

                self._atualizar_elemento(_id, identificador, timeout)

                self._clicar(submit, silent=False, timeout=timeout)

            alert = self.alert_is_present(timeout)

            if alert:
                txt = alert.text
                alert.accept()
                return txt

            else:
                return None

        else:

            self._atualizar_elemento(_id, identificador, timeout=timeout)

            return None

    def _get_acoes(self, helper, keys):
        return tuple(helper.get(x, None) for x in keys)

class Scpx(Sistema):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login=None, senha=None, timeout=10):

        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Scpx

    def consulta(self, identificador, tipo_id="id_cpf", timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ("link", tipo_id, None))  # 'submit'))

        self._navigate(identificador, tipo_id, acoes)

        identificador = functions.strip_string(identificador)

        try:

            self._clicar((By.LINK_TEXT, identificador), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            # print("Não há mais de um registro de Outorga")
            pass

        try:

            self._clicar(h["id_btn_estacao"], timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não há registro para o identificador informado")

            return None

        return True

    def imprime_consulta(self, identificador, tipo_id="id_cpf", resumida=False):

        self.consulta(identificador, tipo_id)

        h = self.sis.consulta

        try:

            if resumida:
                btn_id = h.get("impressao_resumida")
            else:
                btn_id = h.get("impressao_completa")

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return

        self._clicar(btn_id)

    def servico_incluir(
        self, identificador, num_processo, tipo_id="id_cpf", silent=False, timeout=5
    ):

        h = self.sis.servico

        num_processo = functions.strip_string(num_processo)

        acoes = self._get_acoes(h, ("incluir", tipo_id, "submit"))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        self._atualizar_elemento(h.get("id_num_proc"), num_processo, timeout=timeout)

        self._clicar(h.get("id_btn_corresp"), timeout=timeout)

        if silent:
            self._clicar(h.get("submit"), timeout=timeout)

    def servico_excluir(
        self, identificador, documento, motivo="Renúncia", tipo_id="id_cpf"
    ):

        h = self.sis.servico

        acoes = self._get_acoes(h, ("excluir", tipo_id, "submit"))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        alert = self.alert_is_present(2)

        if alert:
            alert.dismiss()

        self._clicar(h.get("id_btn_dados_exclusão"))

        self._atualizar_elemento(h.get("id_doc_exclusão"), documento)

        self._selecionar_por_texto(h.get("id_motivo_exclusão"), motivo)

        self._clicar(h.get("submit"))

        alert = self.alert_is_present(2)

        if alert:
            alert.dismiss()

    def incluir_estacao(
        self,
        identificador,
        tipo_estacao,
        indicativo,
        tipo_id="id_cpf",
        sede=True,
        sequencial="001",
        uf="SP",
        timeout=5,
    ):

        if tipo_estacao not in ESTAÇÕES_RC:
            raise ValueError("Os tipos de estação devem ser: {0}".format(ESTAÇÕES_RC))

        assert functions.check_input(
            indicativo, tipo="indicativo"
        ), "Formato de Indicativo Inválido"

        helper = self.sis.estacao

        acoes = self._get_acoes(helper, ("incluir", tipo_id, "submit"))

        self._navigate(identificador, tipo_id, acoes)

        self._clicar(helper.get("id_btn_dados_estacao"), timeout=timeout)

        self._selecionar_por_texto(helper.get("id_uf"), uf, timeout=timeout)

        alert = self.alert_is_present(timeout=1)

        if alert:
            alert.dismiss()

        self._atualizar_elemento(
            helper.get("id_indicativo"), indicativo, timeout=timeout
        )

        self._atualizar_elemento(helper.get("id_seq"), sequencial, timeout=timeout)

        self._selecionar_por_texto(helper.get("id_tipo"), tipo_estacao, timeout=timeout)

        if tipo_estacao == "Fixa" and sede:
            self._clicar(helper.get("copiar_sede"), timeout=2 * timeout)
            sleep(1)
        self._clicar(helper.get("submit"), timeout=2 * timeout)

    def movimento_transferir(
        self, identificador, origem, dest, proc, tipo_id="id_cpf", timeout=5
    ):

        helper = self.sis.movimento

        links = ("transferir", tipo_id, "submit")

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert:
                alert.accept()

        id_atual = helper.get("id_atual")

        if origem.lower() == "a":

            text = "A - Em análise"

        elif origem.lower() == "b":

            text = "B - Cadastro pela Anatel"

        else:

            print(
                "A transferência de movimento é somente à partir dos Movimentos A ou B"
            )

            return

        self._selecionar_por_texto(id_atual, text, timeout=timeout)

        self._clicar(helper.get("submit"), timeout=timeout)

        if self.check_element_exists(helper.get("id_proc"), timeout=1):
            proc = re.sub("[.-/]", "", proc)

            self._atualizar_elemento(helper.get("id_proc"), proc, timeout=timeout)

        id_posterior = helper.get("id_posterior")

        if dest.lower() == "e":

            self._selecionar_por_texto(
                id_posterior, "E - Aprovado / Licença", timeout=timeout
            )

        elif dest.lower() == "g":

            self._selecionar_por_texto(
                id_posterior,
                "G - Cadastro pelo usuário (auto-cadastramento)",
                timeout=timeout,
            )

            self._atualizar_elemento(
                helper.get("id_txt_cancelar"),
                "Cadastro Incorreto. Estação será refeita com dados corretos",
                timeout=timeout,
            )

        self._clicar(helper.get("submit"), timeout=timeout)

    def movimento_cancelar(self, identificador, tipo_id="id_cpf", timeout: int=10)-> None:

        helper = self.sis.movimento

        links = ("cancelar", tipo_id, "submit")

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert:
                alert.accept()

        self._clicar(helper["id_btn_lista_estacoes"], timeout=timeout/2)

        self._clicar(helper["id_btn_marcar_todos"], timeout=timeout/2)

        self._clicar(helper["submit"], timeout=timeout)

    def licenciar_estacao(
        self, identificador, tipo_id="id_cpf", ppdess=True, silent=False, timeout=5
    ):

        helper = self.sis.estacao

        acoes = self._get_acoes(helper, ("licenciar", tipo_id, "submit"))

        self._navigate(identificador, tipo_id, acoes)

        if tipo_id == "id_cpf":
            self._clicar(
                (By.LINK_TEXT, strip_string(identificador)),
                silent=silent,
                timeout=5 * timeout,
            )

        if not ppdess:
            self._clicar(
                helper.get("id_btn_lista_estacoes"), timeout=timeout, silent=silent
            )

            self._clicar(
                helper.get("id_btn_licenciar"), timeout=timeout, silent=silent
            )

            self._clicar(helper["submit"], timeout=2 * timeout)

            with self._navega_nova_janela():
                self._clicar(helper["marcar_todos"], timeout=timeout)

                self._clicar(helper["btn_print"], timeout=timeout)

    def prorrogar_rf(self, identificador, tipo_id="id_cpf"):

        helper = self.sis.servico

        acoes = self._get_acoes(helper, ("prorrogar_rf", tipo_id, "submit"))

        self._navigate(identificador, tipo_id, acoes)

        self._clicar(helper.get("id_btn_dados_estacao"))

        self._clicar(helper.get("submit"))

        alert = self.alert_is_present(5)

        if alert:
            alert.accept()

    def prorrogar_estacao(self, identificador, tipo_id="id_cpf"):

        helper = self.sis.licenca_prorrogar

        acoes = self._get_acoes(helper, ("link", tipo_id, "submit"))

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException as e:

            print(repr(e))

        alert = self.alert_is_present(timeout=5)

        alert.dismiss()

        self._clicar(helper.get("id_btn_lista_estacoes"))

        self._clicar(helper["submit"])

    def imprimir_licenca(self, identificador, tipo_id="id_cpf", timeout=5):

        helper = self.sis.licenca["imprimir"]

        acoes = self._get_acoes(helper, ("link", tipo_id, "submit"))

        self._navigate(identificador, helper, acoes)

        self._clicar(helper["id_btn_imprimir"], timeout=timeout)

    def extrai_cadastro(self, id, tipo_id="id_cpf", timeout=5):

        self.consulta(id, tipo_id, timeout=timeout)

        dados = {}

        source = soup(self.driver.page_source, "lxml")

        for tr in source.find_all("tr"):

            for td in tr.find_all("td", string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling("td")

                if key not in dados and hasattr(value, "text"):
                    dados[key] = value.text.strip()

        return dados

class Scra(Sistema):
    """
        Esta subclasse da classe Page define métodos de execução de funções nos sistemas
        interativos da ANATEL
    """

    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Scra

    def consulta(self, id, tipo_id="id_cpf", timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ("link", tipo_id, None))  # 'submit'))

        self._navigate(id, tipo_id, acoes)

        id = functions.strip_string(id)

        try:

            self._clicar((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            # print("There is no such element or not found {}".format(id))
            pass

        try:

            self._clicar(h["id_btn_estacao"], timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não há registro para o identificador informado")

            return None

        return True

    def extrai_cadastro(self, id, tipo_id="id_cpf", timeout=5):

        self.consulta(id, tipo_id, timeout=timeout)

        dados = {}

        source = soup(self.driver.page_source, "lxml")

        for tr in source.find_all("tr"):

            for td in tr.find_all("td", string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling("td")

                if key not in dados and hasattr(value, "text"):
                    dados[key] = value.text.strip()

        return dados

    def servico_incluir(
        self, identificador, num_processo, tipo_id="id_cpf", silent=False, timeout=5
    ):

        h = self.sis.servico

        num_processo = functions.strip_string(num_processo)

        acoes = self._get_acoes(h, ("incluir", tipo_id, "submit"))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        self._atualizar_elemento(h.get("id_num_proc"), num_processo, timeout=timeout)

        self._clicar(h.get("id_btn_corresp"), timeout=timeout)

        if silent:
            self._clicar(h.get("submit"), timeout=timeout)

    def movimento_transferir(
        self, identificador, origem, dest, proc, tipo_id="id_cpf", timeout=5
    ):

        helper = self.sis.movimento

        links = ("transferir", tipo_id, "submit")

        acoes = self._get_acoes(helper, links)

        try:

            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            alert = self.alert_is_present(2)

            if alert:
                alert.accept()

        id_atual = helper.get("id_atual")

        if origem.lower() == "a":

            text = "A - Em análise"

        elif origem.lower() == "b":

            text = "B - Cadastro pela Anatel"

        else:

            print(
                "A transferência de movimento é somente à partir dos Movimentos A ou B"
            )

            return

        self._selecionar_por_texto(id_atual, text, timeout=timeout)

        self._clicar(helper.get("submit"), timeout=timeout)

        if self.check_element_exists(helper.get("id_proc"), timeout=1):
            proc = re.sub("[.-/]", "", proc)

            self._atualizar_elemento(helper.get("id_proc"), proc, timeout=timeout)

        id_posterior = helper.get("id_posterior")

        if dest.lower() == "e":

            self._selecionar_por_texto(
                id_posterior, "E - Aprovado / Licença", timeout=timeout
            )

        elif dest.lower() == "g":

            self._selecionar_por_texto(
                id_posterior,
                "G - Cadastro pelo usuário (auto-cadastramento)",
                timeout=timeout,
            )

            self._atualizar_elemento(
                helper.get("id_txt_cancelar"),
                "Cadastro Incorreto. Estação será refeita com dados corretos",
                timeout=timeout,
            )

        self._clicar(helper.get("submit"), timeout=timeout)

    
    

    def extrai_cadastro(self, id, tipo_id="id_cpf", timeout=5):

        dados = {}

        if self.consulta(id, tipo_id, timeout=timeout):

            source = soup(self.driver.page_source, "lxml")

            i = 1

            for tr in source.find_all("tr"):

                for td in tr.find_all("td", string=True):

                    key = td.text.strip(" :")
                    value = td.find_next_sibling("td")

                    if key in dados:

                        key += "_" + str(i)
                        i += 1

                    if hasattr(value, "text"):
                        dados[key] = value.text.strip()

        return dados

    def imprimir_licenca(self, id, tipo_id="id_cpf", timeout=5):
        helper = self.sis.licenca["imprimir"]

        acoes = self._get_acoes(helper, ("link", tipo_id, "submit"))

        self._navigate(id, helper, acoes)

        id = strip_string(id)

        try:

            self._clicar((By.LINK_TEXT, id), timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não foi possível navegar para a página de consulta")

        self._clicar(helper["id_btn_imprimir"])

class Sec(Sistema):

    KEYS = [
        "Dados do Usuário",
        "Dados de Telefones",
        "Endereço Correspondência",
        "Endereço Sede",
        "Certificado",
    ]

    SEC_DADOS = sis_helpers.DADOS

    SEC_DADOS["Certificado"] = [
        "Fistel",
        "Situação",
        "Certificado",
        "Categoria",
        "Data Habilitação",
        "Marca",
        "Boleto Emissão",
        "Boleto 2ªVia",
        "Data Emissão",
        "Usuário Emissão",
        "Data Reemissão",
        "Usuário Reemissão",
        "Certificado Estrangeiro",
        "Validade Certificado",
        "Funcionário OI",
        "Data Inclusão",
        "Usuário_Inclusão",
        "Data_Alteração",
        "Usuário_Alteração",
        "Motivo_Exclusão",
        "Informe_Exclusão",
        "Data_da_Exclusão",
        "Usuário_Exclusão",
        "Status",
        "Observação",
    ]

    SEC_ALT = OrderedDict({
        "Dados do Usuário": [
            # "CNPJ/CPF",
            # "Nome/Razão Social",
            # "Nacionalidade",
            # "Usuário Alteração",
            # "Tipo Usuário",
            "E-mail",
            # "Home Page",
            # "Observação",
        ],
        "Dados Complementares": [
            "Identidade",
            "Órgão Exp.",
            "Sexo",
            "Estado Civil",
            "Data de Nascimento",
            "Num CREA", 
            "Sigla UF_CREA",
            "CNPJ/CPF_Responsável"
        ],
        "Dados de Telefones": ["DDD", "Principal", "DDD2", "Principal2"],
        "Endereço Sede": [
            "País",
            "CEP",
            "Logradouro",
            "Número",
            "Complemento",
            "Bairro",
            "UF",
            "Município",
            "Distrito",
            "Subdistrito",
        ],
    })  # type: Dict[str, List[str]]

    def __init__(
        self, driver: selenium.webdriver, login: str = "", senha: str = "", timeout=2
    ) -> None:
        """Initializes and autenticate the Webdriver instance
        """
        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Sec

    def consulta(self, identificador: str, tipo_id: str = "id_cpf", timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ("link", tipo_id, "submit"))  # 'submit'))

        self._navigate(identificador, tipo_id, acoes)

        identificador = functions.check_input(identificador, tipo_id)

        if tipo_id == "id_cpf":

            if self.check_element_exists(
                (By.LINK_TEXT, identificador), timeout=timeout
            ):

                try:

                    self._clicar((By.LINK_TEXT, identificador), timeout=timeout)

                except (NoSuchElementException, TimeoutException):

                    pass

    def incluir_cadastro(self, dados: dict, menor: bool = False, timeout: int=5) -> bool:
        """[summary]
        
        Args:
            dados (dict): [description]
            menor (bool, optional): Defaults to False. [description]
        
        Returns:
            bool: [description]
        """

        h = self.sis.entidade

        h = h["incluir"]
        acoes = self._get_acoes(h, ("link", "id_cpf", "submit"))
        response = self._navigate(dados["CNPJ/CPF"], h, acoes)

        if response is not None:
            return response
        
        buttons = (h["bt_dados"], h["bt_fone"], h["bt_end"])

        telas = self.SEC_ALT.copy()
        telas.pop("Endereço Sede")
        
        if menor:
            cpf_resp = dados.get("CNPJ/CPF_Responsável", None) 
            #telas["Dados do Usuário"]["cpf_resp"] = cpf_resp
            assert cpf_resp, "É obrigatório informar o CPF do Responsável para menores de 18 anos"

        self._atualizar_elemento(h["input_nome"], 
        dados["Nome/Razão Social"]  + Keys.TAB, timeout=timeout)
        
        for i, (tela, campos) in enumerate(telas.items()):            
            for campo in campos:
                value = dados.get(campo, None)
                if value:
                    self._atualizar_elemento(h[campo], value + Keys.TAB, timeout=timeout)
                
            self._clicar(buttons[i], timeout=timeout)

        cep = dados.get("CEP", "").replace("-", "")        

        assert cep, "É Obrigatório informar o CEP para inclusão de Cadastro"
        response = self._carrega_cep(dados, cep, h)
        if response is not None:
            return response            
        try:

            self._clicar(h["submit"], timeout=timeout)

        except TimeoutException:

            self.driver.execute_script(h["submit_script"])

        alert = self.alert_is_present(timeout=timeout)

        if alert:
            if alert.text == h["atualizar_ok"]:
                alert.accept()
                return None
            else:
                return alert.text

        return None

    def regularizar_RF(self, cpf: str, situacao: str, timeout: int = 10) -> bool:
        """[summary]
        
        Args:
            cpf (str): [description]
        
        Returns:
            bool: [description]
        """
        h = self.sis.entidade["regularizar_RF"]

        acoes = self._get_acoes(h, ("link", "id_cpf", "submit"))

        response = self._navigate(cpf, h, acoes)

        if response is not None:
            return response

        source = soup(self.driver.page_source, "lxml")

        if source.find_all("label", string="0 - Regular"):
            return True

        self._selecionar_por_texto(h["nova_situacao"], text=situacao, timeout=timeout)

        btn = self.wait_for_element_to_click(h["nova_situacao"], timeout=timeout)

        btn.send_keys(2 * Keys.TAB + Keys.RETURN)

        alert = self.alert_is_present(timeout=timeout)

        if alert:
            if alert.text == h["atualizar_ok"]:
                alert.accept()
                return None
            else:
                return alert.text

        # self._click_button(h["submit"], timeout=timeout)

        # self._click_button((By.PARTIAL_LINK_TEXT, "Confirmar"), timeout=timeout)

        return None

    def _carrega_cep(self, dados: dict, cep: str, h: dict, timeout: int=5)-> bool:
        
        self._atualizar_elemento(h["CEP"], cep, timeout=timeout)

        self._clicar(h["bt_cep"], timeout=timeout)

        alert = self.alert_is_present(timeout)

        if alert:
            return alert.text

        uf = self.wait_for_element(h["UF"])

        # After clicking the 'bt_cep' button it takes a while until the uf.value attribute is set
        # until then there is no uf.value
        while uf.get_attribute("value") == "":
            sleep(1)
            uf = self.wait_for_element(h["UF"], timeout=timeout)

        logr = self.wait_for_element_to_be_visible(h["Logradouro"], timeout=timeout)

        # if the CEP loading didn't retrieve the logradouro, update it manually
        if not logr.get_attribute("value"):
            self._atualizar_elemento(h["Logradouro"], dados["Logradouro"].title(), timeout=timeout)

        bairro = self.wait_for_element(h["Bairro"], timeout=timeout)

        if not bairro.get_attribute("value"):
            self._atualizar_elemento(h["Bairro"], dados["Bairro"].title(), timeout=timeout)

        if "Número" not in dados:
            raise ValueError("É obrigatório informar o número do endereço")

        self._atualizar_elemento(h["Número"], dados["Número"], timeout=timeout)

        comp = str(dados.get("Complemento", "")).title()

        self._atualizar_elemento(h["Complemento"], comp,timeout=timeout)

        return None

    def atualiza_cadastro(
        self,
        dados: dict,
        alt_nome: bool = False,
        p_alt: str = None,
        menor: bool = False,
        timeout: int = 5
    ):
        """
        Atualiza os campos retornados pelo dicionário `dados`.
        :param dados: Dicionário com todos os campos  da página (Sec -> Entidade -> Alterar)
        :return: None


        Assuma que as chaves do dicionário casa com os campos da página
        """       

        h = self.sis.entidade
    
        h = h["alterar"]
        acoes = self._get_acoes(h, ("link", "id_cpf", "submit"))
        response = self._navigate(dados["CNPJ/CPF"], h, acoes)

        if response is not None:
            return response
        
        buttons = (h["bt_dados"], h["bt_fone"], h["bt_end"])

        telas = self.SEC_ALT.copy()
        telas.pop("Endereço Sede")
        
        if menor:
            cpf_resp = dados.get("CNPJ/CPF_Responsável", None) 
            #telas["Dados do Usuário"]["cpf_resp"] = cpf_resp
            assert cpf_resp, "É obrigatório informar o CPF do Responsável para menores de 18 anos"

        if alt_nome:
            self._clicar(h["bt_alt_razao"], timeout=timeout)
            self._atualizar_elemento(h["id_novo_nome"], 
                dados["Nome/Razão Social"]  + Keys.TAB, timeout=timeout)
            if p_alt is None:
                p_alt = dados["CNPJ/CPF"]
            self._atualizar_elemento(h["id_p_altera"], p_alt + Keys.TAB, timeout=timeout)

        
        for i, (_, campos) in enumerate(telas.items()):
            for campo in campos:
                value = dados.get(campo, None)
                if value:
                    self._atualizar_elemento(h[campo], value + Keys.TAB, timeout=timeout)
                    

            self._clicar(buttons[i], timeout=timeout)

        cep = dados.get("CEP", "").replace("-", "")        

        if cep:
            response = self._carrega_cep(dados, cep, h)
            if response is not None:
                return response            
        try:

            self._clicar(h["submit"], timeout=timeout)

        except TimeoutException:

            self.driver.execute_script(h["submit_script"])

        alert = self.alert_is_present(timeout=timeout)

        if alert:
            if alert.text == h["atualizar_ok"]:
                alert.accept()
                return None
            else:
                return alert.text

    def consulta_inscrição(self, cpf: str, timeout: int =5)-> None:
        h = self.sis.inscricao["consultar"]

        acoes = self._get_acoes(h, ("link", "id_cpf", "submit"))  # 'submit'))

        response = self._navigate(cpf, h, acoes)

        alert = self.alert_is_present(timeout)

        if alert:
            print(alert.text)
            alert.accept()
            return False


        #if hasattr(response, "text") and response.text == h["not_found"]:
        #    return False

        else:
            #self._click_button(h["imprimir"])

            imprimir = self.wait_for_element_to_click(h["imprimir"], timeout=timeout)

            imprimir.send_keys(Keys.CONTROL + "p")

        alert = self.alert_is_present(timeout)

        if alert:
            alert.accept()

        return True

    def _extrai_inscritos_prova(self):

        dados = OrderedDict()

        source = soup(self.driver.page_source, "lxml")

        base = "http://sistemasnet/SEC/Prova/BancaEspecialImpressao/"

        Inscrito = namedtuple("Inscrito", "link cpf nome coer impresso")

        for tr in source.find_all(
            "tr", id=re.compile("^TRplus.*| ^TRplus2.* | ^TRplus.* | ^TRplus4.*")
        ):
            td = list(tr.find_all("td"))

            assert len(td) >= 5, "O identificador tabular retornado não é válido"

            link = td[0].a.attrs["onclick"].split("'")[1]

            link = base + link

            cpf = td[1].label.text.strip()

            nome = td[0].a.text.strip().upper()

            coer = td[2].label.text.strip()

            impresso = hasattr(td[-1].label, "text") and td[-1].label.text != ""

            dados[cpf] = Inscrito(link, cpf, nome, coer, impresso)

        return dados

    def inscrever_candidato(
        self, cpf, uf, certificado, data, menor=False, protocolo=None, timeout: int=5
    ):

        h = self.sis.inscricao["incluir"]

        self.driver.get(h["link"])

        self._atualizar_elemento(h["id_cpf"], cpf, timeout=timeout)

        self._selecionar_por_texto(h["id_uf"], uf, timeout=timeout)

        self._selecionar_por_texto(h["id_certificado"], certificado, timeout=timeout)

        self._clicar(h["submit"], timeout=timeout)

        sleep(timeout)

        if menor:

            assert protocolo is not None, "Forneça o protocolo de Inscrição do Menor"

            self._atualizar_elemento(h["protocolo"], protocolo, timeout=timeout)

        result = self._clicar((By.LINK_TEXT, data), silent=False, timeout=timeout)

        assert (
            result.text
            == "Confirma inscrição para a agenda selecionada (Data/UF/Certificado) ?"
        ), f"Candidato não foi inscrito, erro: {result}"

        result.accept()

        alerta = self.alert_is_present(timeout=2*timeout).accept()

    def imprimir_provas(self, num_prova, cpf, num_registros, start=0, end=-1, path: str=sis_helpers.PATH, timeout: int=5):

        h = self.sis.Prova["imprimir"]

        link = h["link_direto"].format(num_prova, cpf)

        self.driver.get(link)

        self.driver.execute_script(h["alt_reg"])

        self._atualizar_elemento(h["num_reg"], str(num_registros) + Keys.RETURN, timeout=timeout)

        sleep(timeout)

        dados = self._extrai_inscritos_prova()

        nomes = [n for n in dados.values()]

        for v in nomes[start:end]:

            self.driver.get(v.link)

            alert = self.alert_is_present(timeout=timeout)

            if alert:

                alert.accept()

                self._atualizar_elemento(h["justificativa"], "Erro de Impressão", timeout=timeout)

                self.driver.execute_script("gravarReimprimirProva();")

                alert = self.alert_is_present(timeout=timeout)

                if alert:
                    alert.accept()

                sleep(2)

                self.driver.execute_script("reimprimirprova();")

                alert = self.alert_is_present(timeout=timeout)

                if alert:
                    alert.accept()

                alert = self.alert_is_present(timeout=timeout)

                if alert:
                    alert.dismiss()

            else:
                # self._click_button(h['id_bt_imprimir'], timeout =10)

                self.driver.execute_script("imprimirprova();")

                alert = self.alert_is_present(timeout=timeout)

                if alert:
                    alert.accept()

            sleep(timeout)

            files = sorted(os.listdir(path))

            file = os.path.join(path, files[0])

            os.rename(file, os.path.join(path, str(v.nome).upper() + ".pdf"))

    def extrai_cadastro(self, id, tipo_id="id_cpf", timeout=5):
        def soup_clean(source):

            ids = [
                "ImgObrigatorioIndCertificadoEstrangeiro",
                "msgIndCertificadoEstrangeiro",
            ]

            labels = source.find_all("label")

            for label in source.find_all("label"):

                if "id" in label.attrs and label.attrs["id"] in ids:

                    labels.remove(label)

            is_estrangeiro_sim = source.find("IndCertificadoEstrangeiro0")

            is_estrangeiro_nao = source.find("IndCertificadoEstrangeiro1")

            is_estrangeiro = hasattr(is_estrangeiro_sim, "CHECKED")

            if is_estrangeiro:

                labels.pop(is_estrangeiro_nao)
            else:
                labels.pop(is_estrangeiro_sim)

            return [l.text.strip().strip(":") for l in labels]

        self.consulta(id, tipo_id, timeout=timeout)

        source = soup(self.driver.page_source, "lxml")

        sem_cadastro = (
            r"Não foi encontrado nenhum registro com os critérios informados!"
        )

        if source.find(string=re.compile(sem_cadastro)):
            return {}

        dados = soup_clean(source)

        cadastro = OrderedDict()

        dados = [d for d in dados if d != "Categoria"]

        for i, key in enumerate(self.KEYS[:-1]):

            start = dados.index(key) + 1

            end = dados.index(self.KEYS[i + 1])

            cadastro[key] = OrderedDict(zip(self.SEC_DADOS[key], dados[start:end]))

        key = self.KEYS[-1]

        dados = dados[end + 1 :]

        cadastro[key] = OrderedDict(zip(self.SEC_DADOS[key], dados))

        return cadastro

        # for tr in source.find_all('tr'):
        #
        #     for td in tr.find_all('td', string=True):
        #
        #         i = 1
        #
        #         key = td.text.strip(" :")
        #         value = td.find_next_sibling('td')
        #
        #         # TODO: Adaptar para tabulação referente às provas
        #         if key in dados:
        #             i += 1
        #             key += str(i)
        #
        #         if hasattr(value, 'text'):
        #             dados[key] = value.text.strip()

        # return OrderedDict(dados.items(), key=lambda t: t[0])

    def alterar_nome(self, cpf, novo):

        pass

class Slmm(Sistema):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login=None, senha=None, timeout=10):

        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Slmm

    def consulta(self, identificador, tipo_id="id_cpf", timeout=5):

        h = self.sis.consulta

        acoes = self._get_acoes(h, ("link", tipo_id, None))  # 'submit'))

        self._navigate(identificador, tipo_id, acoes)

        identificador = functions.strip_string(identificador)

        try:

            self._click_button(h["id_btn_estacao"], timeout=timeout)

        except (NoSuchElementException, TimeoutException):

            print("Não há registro para o identificador informado")



    def servico_excluir(
        self, identificador, documento, 
        motivo="Renúncia", tipo_id="id_cpf", num_proc=None, timeout=10
    ):

        h = self.sis.servico

        acoes = self._get_acoes(h, ("excluir", tipo_id, "submit"))

        try:
            self._navigate(identificador, tipo_id, acoes)

        except UnexpectedAlertPresentException:

            print("Alerta Inesperado")

        alert = self.alert_is_present(2)

        if alert:
            alert.dismiss()

        proc = self.wait_for_element(h.get("id_num_proc"), timeout=timeout)

        if self.check_element_exists(h.get("id_num_proc"), timeout=timeout):
            self._atualizar_elemento(h.get("id_num_proc"), num_proc, timeout=timeout)

        self._click_button(h.get("id_btn_dados_exclusão"), timeout=timeout)

        self._atualizar_elemento(h.get("id_doc_exclusão"), documento, timeout=timeout)

        self._selecionar_por_texto(h.get("id_motivo_exclusão"), motivo, timeout=timeout)

        self._click_button(h.get("submit"), timeout=timeout)

        alert = self.alert_is_present(2)

        if alert:
            alert.dismiss()

        
class Sigec(Sistema):
    def __init__(self, driver, login="", senha="", timeout=2):

        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Sigec

    def extrai_cadastro(self, id, tipo_id="id_cpf"):

        self.consulta_geral(id, tipo_id, 30)

        dados = {}

        source = soup(self.driver.page_source, "lxml")

        for tr in source.find_all("tr"):

            for td in tr.find_all("td", string=True):

                key = td.text.strip(" :")
                value = td.find_next_sibling("td")

                if key not in dados:
                    dados[key] = value.text.strip()

        return dados

    def consulta_geral(self, ident, tipo_id="id_cpf", timeout=5, simples=True):

        h = self.sis.consulta["geral"]

        acoes = self._get_acoes(h, ("link", tipo_id, "submit"))

        if not simples:
            pass

        self._navigate(ident, tipo_id, acoes)

class Boleto(Sistema):
    def __init__(self, driver, login=None, senha=None, timeout=5):

        super().__init__(driver, login, senha, timeout)

        self.sis = sis_helpers.Boleto

    def imprime_boleto(self, ident, tipo_id="id_cpf", timeout=5):
        """ This function receives a webdriver object, navigates it to the
        helpers.Boleto page, inserts the identification 'ident' in the proper
        field and commands the print of the boleto
        """

        # acoes = self._get_acoes(h, ('link', tipo_id, 'submit'))

        h = self.sis.imprimir

        ident = strip_string(ident)

        self.driver.get(h["link"])

        if tipo_id == "id_cpf":

            input_ = h["input_cpf"]

            self._clicar(h[tipo_id], timeout=timeout)

        elif tipo_id == "id_fistel":

            input_ = h["input_fistel"]

        self._atualizar_elemento(input_, ident, timeout=timeout)

        self._atualizar_elemento(
            h["input_data"], functions.last_day_of_month(), timeout=timeout
        )

        self._clicar(h["submit"], timeout=timeout)

        self._clicar(h["marcar_todos"], timeout=timeout)

        self._clicar(h["btn_print"], timeout=timeout)


def abrir_agenda_prova(sec, datas):
    for data in datas:
        sec.driver.get(sis_helpers.Sec.Agenda_Incl)

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.data)
        elem.send_keys(data[0])

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.hora)
        elem.send_keys(data[1])

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.avaliador)
        elem.send_keys("31888916877")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.local)
        elem.send_keys("ANATEL SP. Proibido Bermuda e Regata")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.ddd)
        elem.send_keys("11")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.fone)
        elem.send_keys("Somente pelo Fale Conosco em www.anatel.gov.br")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.responsavel)
        elem.send_keys("Ronaldo S.A. Batista")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.vagas)
        elem.send_keys("4")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.morse)
        elem.click()

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.pc)
        elem.click()

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.dias)
        elem.send_keys("1")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.btn_endereco)
        elem.click()

        sleep(1)

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.cep)
        elem.send_keys("04101300")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.btn_buscar_end)
        elem.click()

        sleep(5)

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.numero)
        elem.send_keys("3073")

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.btn_certificado)
        elem.click()

        sleep(1)

        elem = Select(sec.wait_for_element_to_click(sis_helpers.Agenda.select_cert_1))
        elem.select_by_visible_text(
            "Certificado de Operador de Estação de Radioamador-Classe A"
        )

        sec.driver.execute_script("AdicionarCertificado('');")
        sleep(1)

        elem = Select(sec.wait_for_element_to_click(sis_helpers.Agenda.select_cert_2))
        elem.select_by_visible_text(
            "Certificado de Operador de Estação de Radioamador-Classe C"
        )

        elem = sec.wait_for_element_to_click(sis_helpers.Agenda.btn_confirmar)
        elem.click()

        try:

            alert = sec.alert_is_present(5)

            sleep(2)

            alert.accept()

        except TimeoutException:

            print("Não foi possível aceitar o alerta")
