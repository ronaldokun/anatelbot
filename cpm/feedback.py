import pandas as pd

import re
# Access and edit Google Sheets by gspread
import gspread

# Module to transform gsheets to data frame
import gspread_dataframe as gs_to_df

from oauth2client.service_account import  ServiceAccountCredentials

import datetime as dt


TEMPLATE = "Feedback_Template"

MATRICULA = "3. Planilha Matrículas 2018 - 1o sem"

MATR_ABA = "JoãoXXIII"

COLUNAS = ["Data_Pré_Matrícula",\
           "Hora_Pré_Matrícula",\
           "Turma",\
           "Código de Matrícula",\
           "Nome",\
           "Último Nível Cursado na CPM",\
           "Data de Nascimento",\
           "RG",\
           "E-mail",\
           "Tel_Fixo",\
           "Tel_Celular",\
           "Já fez inglês fora da escola?",\
           "Nome Responsável",\
           "Celular_Responsável",\
           "Fez a Pré Matrícula Online?",\
           "Confirmou a Matrícula Presencialmente?",\
           "Matrícula ou Rematrícula",\
           "Algum Documento Faltante?",\
           "Termo de Uso de Imagem Assinado?",\
           "Fila de Espera",\
           "Possui Algum Parente na ONG?",\
           "Quantos?",\
           "Observações",\
           "Student precisa de novo livro (ex: turmas C, E, G e I ou new student)?",\
           "Student recebeu o livro?",\
           "Student DESISTIU? (Student se matriculou, mas NÃO comareceu a nenhuma aula)(SIM/NÃO)",\
           "Se SIM, Por que?",\
           "Se SIM, Por que?.1",\
           "Student EVADIU? (Student compareceu a pelo menos 1 aula, e desistiu depois disso)(SIM/NÃO)",\
           "Se SIM, Por que?.3",\
           "Student foi aprovado para o próximo nível?"]


def authenticate():

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    #Configurations necessary to gspread to work
    credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    gc = gspread.authorize(credentials)

    return gc


def load_sheet_to_df(gc, name, aba, skiprows=None):

    wks = gc.open(name).worksheet(aba)

    col_names = [col for col in wks.row_values(1) if col != '']

    df = gs_to_df.get_as_dataframe(joao, skiprows=skiprows, dtype=str)

    df = df[col_names]

    return df

    #df.to_csv(name, sep=",", index=False)

def check_feedback(gc, name):

    aloc = gc.open('Alocação')


    # Convert gsheet to df
    aloc = gs_to_df.get_as_dataframe(aloc, dtype=str)


    # Transform String Dates to datetime
    f = lambda x : dt.datetime.strptime(x, "%d/%m/%Y")

    aloc['Data'] = aloc['Data'].map(f)

    # correct 'nan' strings to ''
    aloc.replace('nan', '', inplace=True)






def split_date_hour(col):

    return pd.Series(col.split(" "))


def concat_names(x,y):

    return x + " " + y


def split_celfone(col):

    if type(col) == str:

        pattern = ".*\(.*(\d{2})\).*(\d{5})(\d{4}).*"

        split = re.split(pattern, col)

        if len(split) >= 4:

            return "(" + split[1] + ")" + " "  + split[2] + "-" + split[3]

        return col

    return col

def split_fone(col):

    if type(col) == str:

        pattern = ".*\(.*(\d{2})\).*(\d{4}|\d{4})(\d{4}).*"

        split = re.split(pattern, col)

        if len(split) >= 4:

            return "(" + split[1] + ")" + " "  + split[2] + "-" + split[3]

        return col

    return col

def preprocess_df(df):

    presencial = df["Data e hora pré-matrícula online"] == "Presencial"

    espera = df["Data e hora pré-matrícula online"] == "Lista de Espera"

    pre = df[~ presencial & ~ espera]["Data e hora pré-matrícula online"]

    data_hora = pre.apply(split_date_hour)

    data = pd.Series.append(df[presencial]["Data e hora pré-matrícula online"],
                            df[espera]["Data e hora pré-matrícula online"])

    data = data.append(data_hora.iloc[:, 0]).sort_index()

    hora = pd.Series.append(df[presencial]["Data e hora pré-matrícula online"],
                            df[espera]["Data e hora pré-matrícula online"])

    hora = hora.append(data_hora.iloc[:, 1]).sort_index()

    df.rename(columns={"Data e hora pré-matrícula online": "Data_Pré_Matrícula"},
              inplace=True)

    df["Data_Pré_Matrícula"] = data

    df["Hora_Pré_Matrícula"] = hora

    df["Nome"] = df["Nome"].apply(str.upper).apply(str.strip)

    df["Sobrenome"] = df["Sobrenome"].apply(str.upper).apply(str.strip)

    df["Nome Responsável"] = df["Nome Responsável"].apply(str.upper).apply(str.strip)

    df["Sobrenome Responsável"] = df["Sobrenome Responsável"].apply(str.upper).apply(str.strip)

    df["Nome Responsável"] = concat_names(df["Nome Responsável"],
                                          df["Sobrenome Responsável"])

    del df["Sobrenome Responsável"]

    df["Nome"] = concat_names(df["Nome"], df["Sobrenome"])

    del df["Sobrenome"]

    df.rename(columns={"Telefone Celular ex: (011) 00000-0000": "Tel_Celular"},
              inplace=True)

    df["Tel_Celular"] = df["Tel_Celular"].apply(split_celfone)

    df.rename(columns={"Telefone Fixo ex: (011) 000-0000": "Tel_Fixo"},
              inplace=True)

    df["Tel_Fixo"] = df["Tel_Fixo"].apply(split_fone)

    df.rename(columns={"Celular do Responsável": "Celular_Responsável"},
              inplace=True)

    df["Celular_Responsável"] = df["Celular_Responsável"].apply(split_celfone)

    df.rename(columns={"RG \n(apenas números)" : "RG"}, inplace=True)

    return df


def main():

    gc = authenticate()

    df = load_sheet_to_df(gc, MATRICULA, MATR_ABA, skiprows=[1,2])

    df = df.fillna('')

    df = preprocess_df(df)

    df.to_csv("matricula.csv", sep=",", index=False, columns=COLUNAS, na_rep='')

    df = pd.read_csv("matricula.csv", dtype=str, na_values='')

    matricula = gc.open("Matrículas_JOÃOXXIII_2018_Cleaned")

    wks = matricula.worksheet("JoãoXXIII")

    wks.clear()

    gs_to_df.set_with_dataframe(worksheet=wks, dataframe=df)








