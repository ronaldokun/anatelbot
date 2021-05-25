from seleniumbase import BaseCase

class SwagLabsLoginTests(BaseCase):

    def login_to_swag_labs(self, login, senha):
        """ Login to Swag Labs and verify that login was successful. """
        self.open('http://187.44.203.199')
        self.check_window(name="default", level=0, baseline=False)
        #self.switch_to_alert()
        #self.type("#user-name", login)
        #self.type("#password", senha)
        self.click('input[type="submit"]')

    def test_swag_labs_login(self):
        """ This test checks standard login for the Swag Labs store. """
        login = 'root'
        senha = '#IH4qC0t^S&&KblRS&OTBGViYN73!v3q9Opm2#Rsh*P$brIMr3'
        s = senha[0]
        for c in senha[1:]:
            s += c
            self.login_to_swag_labs(login, s)
#         self.assert_element("div.header_label div.app_logo")
#         self.assert_text("Products", "div.product_label")