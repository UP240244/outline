from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class EmailSentPage(BasePage):

    HEADING = (By.CSS_SELECTOR, "h1")
    BACK_TO_LOGIN_BUTTON = (By.XPATH, "//button[contains(., 'Back to login')]")
    EMAIL_ECHOED = (By.CSS_SELECTOR, "em")

    def is_loaded(self):
        return self.is_element_present(self.HEADING, timeout=10)

    def get_heading_text(self):
        return self.get_element_text(self.HEADING)

    def get_confirmed_email(self):
        return self.get_element_text(self.EMAIL_ECHOED)

    def go_back_to_login(self):
        self.click_element(self.BACK_TO_LOGIN_BUTTON)