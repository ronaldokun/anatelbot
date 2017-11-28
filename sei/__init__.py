# -*- coding: utf-8 -*-
"""
This Module initialize the current directory to be imported and
puts all the imports here for a cleaner initialization
"""


# python modules imports
import os
import re
from datetime import datetime as dt
from datetime import time
from bs4 import BeautifulSoup as soup

import pandas as pd

# INITIALIZE DRIVER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# WAIT AND CONDITIONS METHODS
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# Exceptions
from selenium.common.exceptions import TimeoutException

from getpass import getuser, getpass

# Personal Files
import sei.locators as locators
import sei.functions as functions
import sei.pages as pages

# __all__ = ['loc', 'func', 'pages']

