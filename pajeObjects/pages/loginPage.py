from framework.utils import ElementOperations
from framework.Base.BaseElement import By

class LoginPage:
    def __init__(self):
        self.loginField = ElementOperations.Input(By.XPATH, "//input[@id='index_email']")
        self.passwordField = ElementOperations.Input(By.XPATH, "//input[@id='index_pass']")
        self.confirmButton = ElementOperations.Button(By.XPATH, "//button[@id='index_login_button']")

    def autorize(self, login, password):
       self.loginField.send(login)
       self.passwordField.send(password)
       self.confirmButton.click()
