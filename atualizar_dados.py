import sys
import os
import gc
# Change the directory to reflect the main repository
os.chdir("C:/Users/rsilva/gdrive/projects/programming/automation")
import sistemas
import selenium.webdriver as webdriver
import pandas as pd


if __name__ == '__main__':

    print("\nInsira o arquivo com os dados formatados de acordo com o Sapiens e o intervalo de linhas a serem lidas")

    file = str(sys.argv[1])

    start = int(sys.argv[2])

    end = int(sys.argv[3])

    df = pd.read_excel(file, dtype=str, na_values='nan').fillna("")

    df = df.iloc[start:end]

    df["Data de Nascimento"] = df["Data de Nascimento"].str.replace("-", '')

    df["Complemento"] = df["Complemento"].str.replace('nan', "")

    df["Ano do Óbito"] = df["Ano do Óbito"].str.replace('nan', "")

    sec = sistemas.Sec(webdriver.Ie())

    df['Erros'] = []

    for i in range(total):

        try:
            sec.atualiza_cadastro(df.iloc[i])

        except:

            df.iloc[i]["Erros"] = True

        finally:

            next


    df.to_excel("Relatório_de_Entidades_Alteradas")

    sec.driver.close()

    gc.collect()














