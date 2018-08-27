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


    df["Data de Nascimento"] = df["Data de Nascimento"].str.replace("/", '')
    df["E-mail"] = df["E-mail"].str.lower()
    df["Endereço"] = df["Endereço"].str.title()
    df["Cidade"] = df["Cidade"].str.title()
    df["Bairro"] = df["Bairro"].str.title()
    df["CPF"] = df["CPF"].str.replace("-", "")
    df["Complemento"] = df["Complemento"].str.replace("CS", "").str.replace("nan", "")
    df['DDD'] = df['Fone'].apply(lambda x: x[:2])
    df["Fone"] = df['Fone'].apply(lambda x: x[2:])


    df = df.iloc[start:end]

    sec = sistemas.Sec(webdriver.Firefox(), 'rsilva', "Savorthemom3nts")

    sleep(10)

    df['Erro'] = ""

    counter = 0


    for i in range(df.shape[0]):

        print("Atualizando a Entidade: {0}".format(df.iloc[i]["Nome"]))

        sec.atualiza_cadastro(df.iloc[i])

        #df.loc[i, "Erro"] = True

        #print("Erro - Linha: {0}".format(str(i + start)))

        counter += 1

        if counter > 50:

            sec.close()

            gc.collect()

            sec = sistemas.Sec(webdriver.Firefox(), 'rsilva', "Savorthemom3nts")

            sleep(5)

            counter = 0

        gc.collect()



        #print("Atualizado - Linha: {0}".format(str(i + start)))

    df.to_excel("Relatório_de_Entidades_Alteradas.xlsx", index=False)

    sec.driver.close()

    gc.collect()














