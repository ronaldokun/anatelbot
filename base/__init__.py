# Main package
import selenium
import selenium.webdriver as webdriver

# Exceptions
import selenium.common.exceptions as exceptions

# Utilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Methods used from selenium submodules
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

__all__ = ['selenium',
           'webdriver',
           'exceptions',
           'ActionChains',
           'By',
           'Keys',
           'ec',
           'WebDriverWait']
