# modules only
import re

import unidecode
from bs4 import BeautifulSoup as Soup

import functions
import helpers
from page import *
from time import sleep

SERVICOS = ('Outorga: Rádio do Cidadão',
             'Outorga: Radioamador',
             'Outorga: Limitado Móvel Aeronáutico',
             'Outorga: Limitado Móvel Marítimo')

TRANSLATION = {".":"", "/":"", "-":""}

class make_xlat:
    def __init__(self, *args, **kwds):
        self.adict = dict(*args, **kwds)
        self.rx = self.make_rx( )
    def make_rx(self):
        return re.compile('|'.join(map(re.escape, self.adict)))
    def one_xlat(self, match):
        return self.adict[match.group(0)]
    def __call__(self, text):
        return self.rx.sub(self.one_xlat, text)

strip_processo = make_xlat(TRANSLATION)


def login_sei(driver, usr, pwd):
    """
    Esta função recebe um objeto Webdrive e as credenciais  
    do usuário, loga no SEI - ANATEL e retorna uma instância da classe  
    SEI. 
    """

    browser = Page(driver)
    browser.driver.get(helpers.Login.URL)
    # page.driver.maximize_window()

    usuario = browser.wait_for_element_to_click(helpers.Login.LOG)
    senha = browser.wait_for_element_to_click(helpers.Login.PWD)

    # Clear any clutter on the form
    usuario.clear()
    usuario.send_keys(usr)

    senha.clear()
    senha.send_keys(pwd)

    # Hit Enter
    senha.send_keys(Keys.RETURN)

    return browser.driver



class Sei(Page):
    """
    Esta subclasse da classe Page define métodos de execução de ações na
    página principal do SEI e de resgate de informações
    """

    def __init__(self, driver, processos = {}):
        super().__init__(driver)
        self._processos = processos

    def go(self, link):
        """ Simplifies the navigation of href pages on sei.anatel.gov.br
        by pre-appending the required prefix NAV_URL       """

        self.driver.get(link)

    def get_processos(self):
        return self._processos

    def _set_processos(self, processos):

        self._processos = {strip_processo(p['numero']) : p for p in processos}

    def filter_processos(self, **kwargs):

        processos = {}

        for k,v in kwargs:

            processos = {p : q for p, q in self._processos.items() if p.get(k) == v}

        return processos

    def go_to_processo(self, num):

        striped = strip_processo(num)

        if striped not in self._processos.keys():

            raise ValueError("O processo atual não existe ou não está aberto no SEI")

        self.go(self._processos[striped]['link'])

        return Processo(self.driver, striped, tags=self._processos[striped])

    def see_detailed(self):
        """
        Expands the visualization from the main page in SEI
        """
        try:
            ver_todos = self.wait_for_element_to_click(helpers.Main.ATR)

            if ver_todos.text == "Ver todos os processos":
                ver_todos.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
                  'ver todos os processos'")

        try:

            visual_detalhado = self.wait_for_element_to_click(
                helpers.Main.VISUAL)

            if visual_detalhado.text == "Visualização detalhada":
                visual_detalhado.click()

        except TimeoutException:

            print("A página não carregou no tempo limite ou cheque o link\
            de visualização detalhada")

    def is_init_page(self):
        """Retorna True se a página estiver na página inicial do SEI, False
        caso contrário"""
        return self.get_title() == helpers.Main.TITLE

    def go_to_init_page(self):
        """
        Navega até a página inicial do SEI caso já esteja nela
        a página é recarregada
        Assume que o link está presente em qualquer subpágina do SEI
        """
        self.wait_for_element_to_click(
            helpers.Base.INIT).click()

    def show_lat_menu(self):
        """
        Exibe o Menu Lateral á Esquerda no SEI para acessos aos seus diversos
        links
        Assume que o link está presente em qualquer subpágina do SEI
        """
        menu = self.wait_for_element(helpers.Base.MENU)

        if menu.get_attribute("title") == "Exibir Menu do Sistema":
            menu.click()

    def itera_processos(self):
        """
        Navega as páginas de processos abertos no SEI e guarda as tags
        html dos processos como objeto soup no atributo processos_abertos
        """

        # Apaga o conteúdo atual da lista de processos
        processos = []

        # assegura que está inicial
        if not self.is_init_page():
            self.go_to_init_page()

        # Mostra página com informações detalhadas
        self.see_detailed()

        html_sei = Soup(self.driver.page_source, "lxml")

        processos += html_sei("tr", {"class": 'infraTrClara'})


        try:

            contador = Select(self.wait_for_element(helpers.Main.CONT))

            paginas = [pag.text for pag in contador.options]

            for pag in paginas:
                # One simple repetition to avoid more complex code
                contador = Select(self.wait_for_element(helpers.Main.CONT))
                contador.select_by_visible_text(pag)
                html_sei = Soup(self.driver.page_source, "lxml")
                processos += html_sei("tr", {"class": 'infraTrClara'})

        except TimeoutException:

            print("Só há uma página de processos")

        processos = [functions.armazena_tags(
            [tag for tag in line.contents if tag != '\n'])
            for line in processos]

        self._set_processos(processos)

    def update_elem(self, elem_id, dado):

        elem = self.wait_for_element(elem_id)

        elem.clear()

        elem.send_keys(dado)

    # noinspection PyProtectedMember
    def see_contacts(self, nome):

        nome = unidecode._unidecode(nome)

        if self.get_title() != helpers.Contato.TITLE:
            self.vai_para_pag_contato()

        contato = self.wait_for_element_to_click(helpers.Criar_Processo.CONTATO)

        contato.clear()

        contato.send_keys(nome + Keys.RETURN)

        sleep(5)

        # if not self.elem_is_visible((By.LINK_TEXT, "Nenhum Registro Encontrado")):

        self.wait_for_element_to_be_visible((By.XPATH, "//*[contains(text(), nome)]"))

        html = Soup(self.driver.page_source, 'lxml')

        tags = html.find_all('tr', class_='infraTrClara')

        return (len(tags), tags) if tags else (0, None)

    def update_contacts(self, link, dados):

        self.go(link)

        tipo = Select(self.wait_for_element_to_be_visible(helpers.Contato.TIPO))

        tipo.select_by_visible_text("Pessoa Física")

        self.wait_for_element_to_click(helpers.Contato.PF).click()

        self.update_elem(helpers.Contato.SIGLA, dados['CPF'])

        if dados['SEXO'] == 'MASCULINO':

            self.wait_for_element_to_click(helpers.Contato.MASCULINO).click()

        elif dados['SEXO'] == 'FEMININO':

            self.wait_for_element_to_click(helpers.Contato.FEMININO).click()

        self.update_elem(helpers.Contato.NOME, dados['NOME'])

        self.update_elem(helpers.Contato.END, dados['ENDERECO'] + ' ' + dados['NUM'])

        self.update_elem(helpers.Contato.COMP, dados['COMP'])

        self.update_elem(helpers.Contato.BAIRRO, dados['BAIRRO'])

        uf = Select(self.wait_for_element(helpers.Contato.UF))

        uf.select_by_visible_text(dados['UF'])

        cidade = Select(self.wait_for_element_to_be_visible(helpers.Contato.CIDADE))

        cidade.select_by_visible_text(dados["CIDADE"])

        self.update_elem(helpers.Contato.CEP, dados['CEP'])

        self.update_elem(helpers.Contato.CPF, dados['CPF'])

        self.update_elem(helpers.Contato.RG, dados['RG'])

        self.update_elem(helpers.Contato.ORG, dados['ORG'])

        self.update_elem(helpers.Contato.NASC, dados['NASC'])

        self.update_elem(helpers.Contato.FONE, dados['FONE'])

        self.update_elem(helpers.Contato.CEL, dados['CEL'])

        self.update_elem(helpers.Contato.EMAIL, dados['EMAIL'])

        self.wait_for_element_to_click(helpers.Contato.SALVAR).click()

    def vai_para_pag_contato(self):

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find('li', string='Listar')

        if not tag:
            raise LookupError("The tag of type {0} and string {1} is not present in the page".format('<li>', 'Listar'))

        link = tag.a.attrs['href']

        self.go(link)

    def pesquisa_contato(self, name):

        if self.get_title() != helpers.Pesq_contato.TITLE:

            self.vai_para_pag_contato()

        pesquisa = self.wait_for_element(helpers.Pesq_contato.ID_SEARCH)

        pesquisa.send_keys(name)

        html = Soup(self.driver.page_source, 'lxml')

        tag = html.find_all('td', string=re.compile(".*"+ name+ ".*"))

        print(tag)

    def cria_processo(self, tipo, desc='', inter='', nivel='público'):

        tipo = str(tipo)

        assert tipo in helpers.Criar_Processo.PROCS, \
            print("O tipo de processo digitado {0}, não é válido".format(str(tipo)))

        self.show_lat_menu()

        init_proc = self.wait_for_element_to_click(helpers.Menu.INIT_PROC)

        init_proc.click()

        filtro = self.wait_for_element_to_click(helpers.Criar_Processo.FILTRO)

        filtro.send_keys(tipo)

        # exibe_todos = Sei.wait_for_element_to_click(loc.Tipos.EXIBE_ALL)

        # exibe_todos.click()

        # select = Select(Sei.wait_for_element(loc.Tipos.SL_TIP_PROC))

        tipo = self.wait_for_element_to_click((By.LINK_TEXT, tipo))

        tipo.click()

        if desc:
            espec = self.wait_for_element(helpers.Processo.ESPEC)

            espec.send_keys(desc)

        if inter:

            self.cadastrar_interessado(inter)
            self.consultar_contato(inter)

        if nivel == 'público':

            nivel = self.wait_for_element(helpers.Processo.PUBL)

        elif nivel == 'restrito':

            nivel = self.wait_for_element(helpers.Processo.REST)

        else:

            nivel = self.wait_for_element(helpers.Processo.SIG)

        nivel.click()


class Processo(Sei):

    def __init__(self, driver, numero, tags=None):
        super().__init__(driver)
        self.driver = driver
        self.numero = numero
        self.tags = tags
        self.acoes = {}
        self.tree = {}


    def get_tags(self):
        return self.tags

    def get_acoes(self):

        if self.acoes == {}:

            self._acoes_processo()

        return self.acoes

    def close_processo(self):
        self.driver.close()

    def info_oficio(self, num_doc):
        assert self.get_title() == helpers.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to tree frame
        self.driver.switch_to_frame("ifrArvore")

        with self.wait_for_page_load():
            html_tree = Soup(self.driver.page_source, "lxml")

            info = html_tree.find(title=re.compile(num_doc)).string

            assert info != '', "Falha ao retornar Info do Ofício da Árvore"

            # return to parent frame
            self.driver.switch_to_default_content()

            return info

    def _acoes_processo(self):

        assert self.get_title() == helpers.Processo.TITLE, \
            "Erro ao navegar para o processo"

        # Switch to central frame
        self.driver.switch_to_frame("ifrVisualizacao")

        self.wait_for_element(helpers.Central.ACOES)

        html_frame = Soup(self.driver.page_source, "lxml")

        acoes = html_frame.find(id="divArvoreAcoes").contents

        self.driver.switch_to_default_content()

        self.acoes = functions.cria_dict_acoes(acoes)

    def update_andamento(self, buttons, info):
        assert self.get_title() == helpers.Processo.TITLE, \
            "Erro ao navegar para o processo"

        andamento = buttons[4]

        link = andamento.attrs['href']

        (proc_window, and_window) = Page.nav_link_to_new_win(self.driver, link)

        input_and = self.wait_for_element(helpers.Central.IN_AND)

        text = helpers.Central.AND_PRE + info + helpers.Central.AND_POS

        input_and.send_keys(text)

        self.wait_for_element_to_click(helpers.Central.SV_AND).click()

        self.driver.close()

        self.driver.switch_to_window(proc_window)

    def send_proc_to_sede(self, buttons):

        with self.wait_for_page_load():
            assert self.get_title() == helpers.Processo.TITLE, \
                "Erro na função 'send_proc_to_sede"

            enviar = buttons[3]

            link = enviar.attrs["href"]

            (janela_processo, janela_enviar) = Page.nav_link_to_new_win(
                self.driver, link)

        with self.wait_for_page_load():
            assert self.get_title() == helpers.Envio.TITLE, \
                "Erro ao clicar no botão 'Enviar Processo'"

            self.driver.execute_script(helpers.Envio.LUPA)

            # Guarda as janelas do navegador presentes
            windows = self.driver.window_handles

            janela_unidades = windows[-1]

            # Troca o foco do navegador
            self.driver.switch_to_window(janela_unidades)

        assert self.get_title() == helpers.Envio.UNIDS, \
            "Erro ao clicar na lupa 'Selecionar Unidades'"

        unidade = self.wait_for_element(helpers.Envio.IN_SIGLA)

        unidade.clear()

        unidade.send_keys(helpers.Envio.SIGLA + Keys.RETURN)

        sede = self.wait_for_element(helpers.Envio.ID_SEDE)

        assert sede.get_attribute("title") == helpers.Envio.SEDE, \
            "Erro ao selecionar a Unidade Protocolo.Sede para envio"

        sede.click()

        self.wait_for_element_to_click(helpers.Envio.B_TRSP).click()

        # Fecha a janela_unidades
        self.driver.close()

        # Troca o foco do navegador
        self.driver.switch_to_window(janela_enviar)

        self.wait_for_element_to_click(helpers.Envio.OPEN).click()

        self.wait_for_element_to_click(helpers.Envio.RET_DIAS).click()

        prazo = self.wait_for_element(helpers.Envio.NUM_DIAS)

        prazo.clear()

        prazo.send_keys(helpers.Envio.PRAZO)

        self.wait_for_element_to_click(helpers.Envio.UTEIS).click()

        self.wait_for_element_to_click(helpers.Envio.ENVIAR).click()

        # fecha a janela_enviar
        self.driver.close()

        self.driver.switch_to_window(janela_processo)

    def expedir_oficio(self, num_doc):

        info = self.info_oficio(num_doc)

        buttons = self.acoes_processo()

        self.update_andamento(buttons, info)

        self.send_proc_to_sede(buttons)

    def go_to_postit(self):

        link = self.get_acoes()['Anotações']

        (main, new) = self.nav_link_to_new_win(link)

        return (main, new)

    def edita_postit(self, content='', prioridade=False):

        (main, new) = self.go_to_postit()

        postit = self.wait_for_element(helpers.Central.IN_POSTIT)

        postit.clear()

        postit.send_keys(content)

        prioridade = self.wait_for_element_to_click(helpers.Central.CHK_PRIOR)

        if prioridade:

            if not prioridade.is_selected():

                prioridade.click()

        else:

            if prioridade.is_selected():

                prioridade.click()

        btn = self.wait_for_element_to_click(helpers.Central.BT_POSTIT)

        btn.click()

        self.close()

        self.driver.switch_to_window(main)

        self.tags['anotacao'] = content

        self.tags['anotacao_link'] = ''

    def _incluir_documento(self, tipo):

        if tipo not in helpers.Gerar_Doc.TIPOS:

            raise ValueError("Tipo de Documento inválido: {}".format(tipo))

        link = self.get_acoes().get('Incluir Documento')

        if link:

            with self.wait_for_page_load():

                self.go(link)

            try:

                link = self.wait_for_element_to_click((By.LINK_TEXT, tipo), timeout=5)

            except TimeoutException:

                print("Erro ao navegar para o link Incluir Documento")

            #main, new = self.nav_link_to_new_win(link)

            link.click()

            #return main, new

        else:

            raise ValueError("Problema com o link de ações do processo: 'Incluir Documento'")

    def incluir_oficio(self, tipo, dados, acesso='publico', hipotese=None):

        if tipo not in helpers.Gerar_Doc.TEXTOS_PADRAO:

            raise ValueError("Tipo de Ofício inválido: {}".format(tipo))

        #main, new = self._incluir_documento("Ofício")

        self._incluir_documento("Ofício")

        texto_padrao = self.wait_for_element_to_click(helpers.Gerar_Doc.ID_TXT_PADRAO)

        texto_padrao.click()

        tipos = Select(self.wait_for_element_to_click(helpers.Gerar_Doc.ID_MODELOS_OF))

        tipos.select_by_visible_text(tipo)

        if acesso == 'publico':

            acesso = self.wait_for_element_to_click(helpers.Gerar_Doc.ID_PUB)

            acesso.click()

        elif acesso == 'restrito':

            acesso = self.wait_for_element_to_click(helpers.Gerar_Doc.ID_RES)

            acesso.click()

            hip = Select(self.wait_for_element_to_click(helpers.Gerar_Doc.ID_HIP))

            if hipotese not in helpers.Gerar_Doc.HIPOTESES:

                raise ValueError("Hipótese Legal Inválida: ", hipotese)

            hip.select_by_visible_text(hipotese)

        else:

            raise ValueError("Você provavelmente não vai querer mandar um Ofício Sigiloso")

        confirmar = self.wait_for_element_to_click(helpers.Gerar_Doc.CONFIRMAR)

        confirmar.click()

        self.wait_for_new_window(5)

        windows =  self.driver.window_handles

        janela_processo, janela_oficio = windows[-2], windows[-1]

        self.go(self.get_tags().get('link'))

        self.driver.switch_to_window(janela_oficio)

        self.editar_oficio(dados)

        self.close()

        self.driver.switch_to_window(janela_processo)

    def editar_oficio(self, dados, existing=False):

        for tag, value in dados.items():

            try:

                element = self.wait_for_element((By.LINK_TEXT, tag))

                self.execute_script("arguments[0].innerText = " + value, element)

            except:

                print("Não foi possível editar o elemento: {}".format(tag))

                next
























def exibir_bloco(Sei, numero):
    if Sei.get_title() != loc.Blocos.TITLE:
        Sei.go_to_blocos()

    try:
        Sei.wait_for_element((By.LINK_TEXT, str(numero))).click()

    except:
        print("O Bloco de Assinatura informado não existe ou está \
              concluído!")

def armazena_bloco(Sei, numero):
    if Sei.get_title() != loc.Bloco.TITLE + " " + str(numero):
        Sei.exibir_bloco(numero)

    html_bloco = Soup(Sei.driver.page_source, "lxml")
    linhas = html_bloco.find_all(
        "tr", class_=['infraTrClara', 'infraTrEscura'])

    chaves = ['checkbox', 'seq', "processo", 'documento', 'data', 'tipo',
              'assinatura', 'anotacoes', 'acoes']

    lista_processos = []

    for linha in linhas:

        proc = {k: None for k in chaves}

        cols = [v for v in linha.contents if v != "\n"]

        assert len(chaves) == len(cols), "Verifique as linhas do bloco!"

        for k, v in zip(chaves, cols):
            proc[k] = v

        # proc["expedido"] = False

        lista_processos.append(proc)

    return lista_processos


def expedir_bloco(Sei, numero):

    processos = Sei.armazena_bloco(numero)

    for p in processos:

        if pode_expedir(p):

            proc = p['processo'].a.string

            num_doc = p['documento'].a.string

            link = Sei.go(p['processo'].a.attrs['href'])

            (bloco_window, proc_window) = nav_link_to_new_win(
                Sei.driver, link)

            processo = Processo(Sei.driver, proc_window)

            processo.expedir_oficio(proc, num_doc, link)
