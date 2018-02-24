# Main package
import selenium
import selenium.webdriver as webdriver
# Other modules
from bs4 import BeautifulSoup as Soup

# Exceptions
from selenium.common.exceptions import TimeoutException,\
                                       WebDriverException, \
                                       NoAlertPresentException, \
                                       NoSuchElementException


# Utilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Methods used from selenium submodules
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

__all__ = ['selenium',
           'webdriver',
           'ec',
           'WebDriverWait',
           'ActionChains',
           'By',
           'Keys',
           'Select',
           'TimeoutException',
           'WebDriverException',
           'NoAlertPresentException',
           'NoSuchElementException',
           'Soup']
