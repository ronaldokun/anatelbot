import sys
import os
import gc
from monitor import sleep
# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")
import sistemas
import selenium.webdriver as webdriver
import pandas as pd
from sistemas import *


if __name__ == '__main__':

    #print("\nInsira o arquivo com os dados formatados de acordo com o Sapiens e o intervalo de linhas a serem lidas")

    file = str(sys.argv[1])

    start = int(sys.argv[2])

    end = int(sys.argv[3])

    df = pd.read_excel(file, dtype=str, na_values=['nan', 'Nan']).fillna("")

    df["CPF"] = df["CPF"].str.replace("-", "")

    df = df.iloc[start:end]

    sec = sistemas.Sec(webdriver.Firefox(), 'rsilva', "Savorthemom3nts")

    for _, row in df.iterrows():

        print("Inscrevendo: {0}".format(row["Nome"]))

        cpf = row["CPF"]

        while len(cpf) < 11:

            cpf = '0' + cpf

        uf = 'SP'


        data = "01/09/2018"

        certificado = "Certificado de Operador de Estação de Radioamador-" + row["Classe"]

        try:

            sec.inscrever_candidato(cpf, uf, certificado, data)

        except:

            next


            # if row['Classe'] == "Classe C":
            #
            #     certificado = "Certificado de Operador de Estação de Radioamador-" + 'Classe B'
            #
            #     try:
            #
            #         sec.inscrever_candidato(cpf, uf, certificado, data)
            #
            #     except:
            #
            #
            #         if "Classe B" in certificado:
            #
            #             certificado = certificado = "Certificado de Operador de Estação de Radioamador-" + 'Classe A'
            #
            #             try:
            #
            #                 sec.inscrever_candidato(cpf, uf, certificado, data)
            #
            #             except:






