from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-banner")

    def login(self, user, pwd):
        self.type_text(self.USERNAME_FIELD, user)
        self.type_text(self.PASSWORD_FIELD, pwd)
        self.click_element(self.LOGIN_BUTTON)

    def obtener_error(self):
        return self.find_element(self.ERROR_MESSAGE).text
