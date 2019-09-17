import getpass
from sei import sei
from time import sleep
USR = "rsilva"
PWD = "$@V05!tntlaaE"

def test_login_Chrome():
    try:
        browser = sei.login_sei(USR, PWD, "Chrome")
    finally:
        del browser

def test_login_firefox():
    sei.login_sei(USR, PWD, "Firefox")
