from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def login(self, user, pwd):
        self.type_text(self.USERNAME_FIELD, user)
        self.type_text(self.PASSWORD_FIELD, pwd)
        self.click_element(self.LOGIN_BUTTON)
