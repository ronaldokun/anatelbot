from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import WebDriverWait
from fire import Fire


def autologin(driver, username, password, url="https://sei.anatel.gov.br", delay=5):
    if driver.lower() == "chrome":
        driver = webdriver.Chrome(options=options)

    driver.get(url)
    try:
        password_input = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(("xpath", "//input[@type='password']"))
        )
        print("Page is ready!")
    except TimeoutException:
        print("Timeout")
    password_input.send_keys(password)
    username_input = password_input.find_element_by_xpath(
        ".//preceding::input[not(@type='hidden')]"
    )
    username_input.send_keys(username)
    form_element = password_input.find_element_by_xpath(".//ancestor::form")
    submit_button = form_element.find_element_by_xpath(".//*[@type='submit']").click()
    return driver


if __name__ == "__main__":

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = Fire(autologin)
    driver.save_screenshot("sei.png")
    driver.quit()
