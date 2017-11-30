

from analise.functions import *


def save_source(browser, df, path, start, end):

    for i in range(start,end):

        ident = df.iloc[i]['Fistel']

        consultaScpx(browser, ident, tipo='fistel')

        # devedores.append(name)
        windows = browser.driver.window_handles

        main = windows[0]

        browser.driver.switch_to_window(windows[-1])

        save_page(browser.driver, path + ident + '.html')

        #ie.driver.close()

        #ie.driver.switch_to_window(main)



if __name__ == 'main':

    dtype_dic = {'CPF': str, 'Fistel': str}

    df = pd.read_table('files/cassacao.tsv', dtype=dtype_dic)

    driver = webdriver.Ie()

    browser = Page(driver)

    path = r"C:\Users\rsilva\Google Drive\projects\programming\automation\files\pages"

    save_source(browser, df, path, 100, 200)


