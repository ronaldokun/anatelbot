# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# Standard Lib imports
import sys
from pathlib import Path

# Local application imports
from tool.functions import get_browser

parent = Path("__file__").cwd().parent
sys.path.append(f"{parent}")

# Third party imports


# %load_ext autoreload
# %autoreload 2

# %%
def test_init_default(is_headless=False):
    browser = get_browser(is_headless=is_headless)
    browser.close()


# %%
def test_init_chrome(is_headless=False):
    browser = get_browser("chrome", is_headless=is_headless)
    browser.close()


# %%
def test_init_firefox(is_headless=False):
    browser = get_browser("firefox", is_headless=is_headless)
    browser.close()


# %%
def test_init_ie(is_headless=False):
    browser = get_browser("ie", is_headless=is_headless)
    browser.close()


# %%
def test_init_edge(is_headless=False):
    browser = get_browser("edge", is_headless=is_headless)
    browser.close()


# %%
def test_init_custom_exec(is_headless=False):
    custom_firefox = r"C:\Users\rsilva\Firefox_ESR\firefox.exe"
    browser = get_browser(
        "Firefox", is_headless=is_headless, firefox_binary=custom_firefox
    )
    browser.close()


def test_headless():
    test_init_default(True)
    test_init_chrome(True)
    test_init_firefox(True)
    test_init_ie(True)
    test_init_edge(True)
