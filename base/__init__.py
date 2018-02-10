# Main package
import selenium

import selenium.webdriver as webdriver

# Methods used from selenium submodules
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Exceptions
from selenium.common.exceptions import TimeoutException, \
    WebDriverException
# Other modules
from bs4 import BeautifulSoup as Soup

__all__ = ['wd', 'ec', 'WebdriverWait', 'ActionChains',
           'By', 'Select', 'TimeoutException',
           'WebDriverException', 'Soup']
