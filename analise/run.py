

from os.path import exists

from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By

from analise.functions import *


def save_source(browser, df, path, start, end):

    for i in range(start,end):

        ident = df.iloc[i]['Fistel']

        if exists(path + '/' + ident + '.html'):
            next

        consultaScpx(browser, ident, tipo='fistel')

        # devedores.append(name)
        windows = browser.driver.window_handles

        main = windows[0]

        browser.driver.switch_to_window(windows[-1])

        try:

            save_page(browser.driver, path + '/' + ident + '.html')

        #ie.driver.close()

        #ie.driver.switch_to_window(main)

        except:
            next



def main():

    dtype_dic = {'CPF': str, 'Fistel': str}

    df = pd.read_table('files/cassacao.tsv', dtype=dtype_dic)

    driver = webdriver.Ie()

    browser = Page(driver)

    path = r"C:\Users\rsilva\Google Drive\projects\programming\automation\files\pages"

    save_source(browser, df, path, 0, df.shape[0])


def sigec():

    # erro = []

    # devedores = []

    dtype_dic = {'ENTIDADE':str, 'CPF/CNPJ': str, 'FISTEL': str}

    df = pd.read_csv('files/prescricao_devedores.csv', dtype=dtype_dic)

    #df['DEVEDORES'] = pd.Series(['' for i in range(df.shape[0])], index=df.index)

    null = df["DEVEDORES"].isnull()

    # There is a better way certainly
    for i in df[null].index:
        fistel = df.loc[i,"FISTEL"]
        if '/' in fistel:
            fistel = fistel.split('/')
            #print(fistel)
            copy = df.loc[i].copy()
            df.loc[i,'FISTEL'] = fistel[0]
            copy["FISTEL"] = fistel[1]
            df = df.append(copy, ignore_index=True)
            print(df.shape)

    null = df["DEVEDORES"].isnull()

    driver = webdriver.Chrome()

    browser = Page(driver)



    for i in df[null].index:

        try:

            fistel = df.iloc[i]['FISTEL']

            consultaSigec(browser, fistel, tipo='fistel')

            browser.wait_for_element_to_be_visible((By.ID , "objInicial1"))

            html = soup(browser.driver.page_source, 'lxml')

            resultado = html.find('tr', id=re.compile("TRplus"))

            children = [tag.text for tag in resultado.descendants if tag.name =='td' and tag != '\n']

            children = [re.sub(r'\s', '', text) for text in children]

            # devedores.append(children[9])

            df.set_value(i,'DEVEDORES', children[9])

            print("Linha: ", i)

        except:

            print("Erro na página, linha {}".format(i))

        finally:

            next

    #df["DEVEDORES"] = pd.Series(devedores, index=df.index)

    return df

# df = sigec()
#
# df.to_csv("prescricao_devedores.csv")
#
# writer = pd.ExcelWriter('Prescricao_Devedores.xlsx')
#
# df.to_excel(writer, "05.12.2017", index_label=False)
#
# writer.save()

# main()
