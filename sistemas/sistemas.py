import re

from page import *
from page.page import Page
from sistemas import locators

SERVIÇOS = ['ra', 'px', 'ma', 'mm', 'boleto', 'sec']

classes = {"ra":locators.Scra, "px": locators.Scpx, 'ma': locators.Slma,
           "mm": locators.Slmm, 'boleto': locators.Boleto, 'sec': locators.Sec}

class Sis(Page):
    """
    Esta subclasse da classe Page define métodos de execução de funções nos sistemas
    interativos da ANATEL
    """

    def __init__(self, driver, login, senha):

        super().__init__(driver)

        self.auth = self._authenticate(login, senha)

    def _authenticate(self, login, senha):

        self.driver.get('http://sistemasnet')

        alert = self.alert_is_present(timeout=5)

        if alert:

            try:

                alert.send_keys(login + Keys.TAB + senha)  # alert.authenticate is not working

                alert.accept()

                return True

            except:

                return False

        return True

    def check_input(self, ident, serv, tipo):
        """
        This function parse the data to the ANATEL sistemas

        :param ident: string - the input to navigate the systems:
        :param serv: string - one of the intranet pages defined in SERVIÇOS
        :param tipo: check if it's one of the 3 valid types = 'cpf', 'fistel', 'indicativo'
        :return: The input if the parse went smooth, otherwise ValueError
        """

        ident = str(ident)

        serv = str(serv)

        tipo = str(tipo)

        if serv not in SERVIÇOS:

            raise ValueError("Os Serviços disponíveis para consulta são {}".format(SERVIÇOS))

        if (tipo == 'cpf' or tipo == 'fistel') and len(ident) != 11:

            raise ValueError("O número de dígitos do {0} deve ser 11".format(tipo))

        elif tipo == 'cnpj' and len(ident) != 14:

            raise ValueError("O número de dígitos do {0} deve ser 14".format(tipo))

        elif tipo == 'indicativo':

            if serv in ("boleto", "sec"):
                raise ValueError(
                    "Não esta disponível consulta por Indicativo no serviço {}, use cpf/fistel".format(serv))

            elif serv == "px":

                pattern = r'^(P){1}(X){1}(\d){1}([C-Z]){1}(\d){4}$'

            elif serv == 'ra':

                pattern = r'^(P){1}(U|Y){1}(\d){1}([A-Z]){2,3}$'

            elif serv == "ma":

                pattern = r'^(P){1}([A-Z]){4}$'

            elif serv == "mm":

                pattern = r'^(P){1}([A-Z]{3}|[A-Z]{1}\d{3})'

            if not re.match(pattern, ident, re.I):

                raise ValueError("Indicativo Digitado Inválido")

        return (ident, tipo, classes[serv])

    def _navigate(self, link, ident, id_elem):
        """
        This is a simple wrapper to navigate the anatel systems page

        :param link: string with the link to follow
        :param ident: id ty
        :param id_type:
        :return:
        """

        self.driver.get(link)

        try:

             elem = self.wait_for_element_to_click(id_elem, timeout=5)

             elem.send_keys(ident + Keys.RETURN)

        except NoSuchElementException:

             print("The html id: {} is not present on this webpage".format(ident))

    def consulta(self, ident, serv, id_type):

        ident, id_type, sis = check_input(ident, serv, id_type)

        self._navigate(sis.Consulta['link'], ident, sis.Consulta['id'])


class Px(Sis):

    def __init__(self, driver, login, senha):

        super().__init__(driver, login, senha)

        self.serv = 'px'

    def consulta(self, ident, id_type):

            super().consulta(ident, self.serv, id_type)


    def imprime_consulta(self, ident, serv, id_type):

        self.consulta(ident, serv, id_type)

        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatEstação"))

            elem.click()

        except:

            print("Não foi possível clicar no botão 'Estação' na página consulta")

            return

        try:

            elem = self.wait_for_element_to_click((By.ID, "botaoFlatVersãoparaImpressão"),
                                                  timeout=5)

            elem.click()

        except:

            print("Não foi possível clicar no Botão 'Versão para Impressão")

            return

