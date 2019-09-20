# Standard Library Imports
import re
from typing import Union

# Third party imports
import bs4

URL = "https://sei.anatel.gov.br/sei/"


# https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
def xpath_soup(element: Union[bs4.element.Tag, bs4.element.NavigableString]) -> str:
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if 1 == len(siblings)
            else "%s[%d]"
                 % (child.name, next(i for i, s in enumerate(siblings, 1) if s is child))
        )
        child = parent
    components.reverse()
    return "/%s" % "/".join(components)


def dict_to_df(processos):
    """Recebe a lista processos contendo um dicionário das tags de cada
    processo aberto no SEI. Retorna um Data Frame cujos registros
    são as string das tags.
    """

    cols = [
        "processo",
        "tipo",
        "atribuicao",
        "marcador",
        "anotacao",
        "prioridade",
        "peticionamento",
        "aviso",
        "situacao",
        "interessado",
    ]

    df = pd.DataFrame(columns=cols)

    for p in processos:
        df = df.append(pd.Series(p), ignore_index=True)

    df["atribuicao"] = df["atribuicao"].astype("category")
    df["prioridade"] = df["prioridade"].astype("category")
    df["tipo"] = df["tipo"].astype("category")

    return df


def tag_controle(tag):
    key, value = "", ""

    img = str(tag.img["src"])

    pattern = re.search("\((.*)\)", tag.attrs.get("onmouseover"))

    if "imagens/sei_anotacao" in img:

        # Separa o texto interno retornado pelo js onmouseover delimitado
        # pelas aspas simples. Salvo somente o primeiro e terceiro items

        value = pattern.group().split("'")[1:4:2]

        key = "postit_red" if "prioridade" in img else "postit"

    elif "imagens/sei_situacao" in img:

        key = "situacao"
        value = pattern.group().split("'")[1]

    elif "imagens/marcador" in img:

        marcador = pattern.group().split("'")[1:4:2]
        key = "marcador"
        value = "".join(marcador)

    elif "imagens/exclamacao" in img:

        key = "aviso"
        value = True

    return key, value


def pode_expedir(linha: dict) -> bool:
    """Verifica se a linha do Bloco de Assinatura do Sei está assinada
    
    Args:
        linha (dict): Dicionário com as informações da Linha do Bloco: Processo, tipo, assinatura, 
    
    Returns:
        bool
        True, 
            * Se o Processo está Aberto,
            * Se Tipo = Ofício
            * Contém assinatura Coordenador/Gerente
        False,
        Se um dos casos acima falhar
    """

    t1 = linha["processo"].find_all("a", class_="protocoloAberto")

    t2 = linha["tipo"].find_all(string="Ofício")

    t3 = linha["assinatura"].find_all(string=re.compile("Coordenador"))

    t4 = linha["assinatura"].find_all(string=re.compile("Gerente"))

    return bool(t1) and bool(t2) and (bool(t3) or bool(t4))


def cria_dict_acoes(acoes: list) -> dict:

    """Recebe uma lista de html tags 'a' e retorna um dicionário dessas tags
    
    Args:
        acoes (list): HTML 'a' tags
    
    Returns:
        dict: Dicionário - key=tag title, value= tuple ('xpath', xpath)
    """
    return {tag.contents[0].attrs["title"]: ("xpath", xpath_soup(tag)) for tag in acoes}


def tag_mouseover(tag, tipo: str):
    # TODO: Document with bs4 type

    tag_split = tag.attrs["onmouseover"].split("'")

    if tipo in ("anotacao", "marcador"):

        return " ".join(tag_split[1:4:2])

    elif tipo == "situacao":

        return tag_split[1]

    else:

        raise ValueError("O tipo de tag repassado não é válido: {}".format(tipo))


def armazena_tags(lista_tags: list) -> dict:
    """Recebe uma lista de tags de cada linha do processo  da página inicial
    do Sei, retorna um dicionário dessas tags
    
    Args:
        lista_tags (list): Lista de Tags contida na tag tabular definida por 
        cada linha de processo da página inicial do SEI
    
    Returns:
        dict: dicionário - key=Nome da Tag, value=string ou objeto tag
    """

    assert (
        len(lista_tags) == 6
    ), "Verifique o nº de tags de cada linha do \
        processo: {}. O valor diferente de 6".format(
        len(lista_tags)
    )

    dict_tags = {}

    dict_tags["checkbox"] = lista_tags[0].find("input", class_="infraCheckbox")

    controles = lista_tags[1].find_all("a")

    dict_tags["aviso"] = ""

    for tag_a in controles:

        img = str(tag_a.img["src"])

        if "imagens/sei_anotacao" in img:

            dict_tags["anotacao"] = tag_mouseover(tag_a, "anotacao")

            dict_tags["anotacao_link"] = URL + tag_a.attrs["href"]

        elif "imagens/sei_situacao" in img:

            dict_tags["situacao"] = tag_mouseover(tag_a, "situacao")

            dict_tags["situacao_link"] = URL + tag_a.attrs["href"]

        elif "imagens/marcador" in img:

            dict_tags["marcador"] = tag_mouseover(tag_a, "marcador")

            dict_tags["marcador_link"] = URL + tag_a.attrs["href"]

        elif "imagens/exclamacao" in img:

            dict_tags["aviso"] = True

        peticionamento = lista_tags[1].find(src=re.compile("peticionamento"))

        if peticionamento:

            pattern = re.search("\((.*)\)", peticionamento.attrs["onmouseover"])
            if pattern:
                dict_tags["peticionamento"] = pattern.group().split('"')[1]

        else:

            dict_tags["peticionamento"] = ""

    processo = lista_tags[2].find("a")

    dict_tags["link"] = URL + processo.attrs["href"]

    dict_tags["numero"] = processo.string

    dict_tags["visualizado"] = (
        True if processo.attrs["class"] == "processoVisualizado" else False
    )

    tag = lista_tags[3].find("a")

    dict_tags["atribuicao"] = tag.string if tag else ""

    dict_tags["tipo"] = lista_tags[4].string

    tag = lista_tags[5].find(class_="spanItemCelula")

    dict_tags["interessado"] = tag.string if tag else ""

    return dict_tags


# TODO: Deprecated
def string_endereço(dados, extra=True):
    d = {}

    s = "A(o)<br>"

    s += f'<b>{dados["Nome/Razão Social"].upper()}</b>'

    s += "<br>" + dados["Logradouro"].title() + ", " + dados["Número"] + " "

    s += dados["Complemento"].title() + " "

    s += dados["Bairro"].title() + "<br>"

    s += (
        "CEP: "
        + dados["Cep"]
        + " - "
        + dados["Município"].title()
        + " - "
        + dados["UF"]
    )

    if extra:

        s += "<br><br>" + "<b>FISTEL: " + dados["Fistel"] + "</b>"

        s += "<br>" + "<b>Validade: " + dados["Validade"] + "</b>"

        s += "<br>" + "<b>Indicativo: " + dados["Indicativo"] + "</b>"

        debitos = dados["Entidade Devedora"].upper()

        if debitos == "SIM":
            color = r"#FF0000"
        else:
            color = r"#0000FF"

        s += f'<br><b>Possui débitos? : <span style="color:{color};">{debitos}</span></b>'

    d["À"] = s

    return d
