from selenium.webdriver.common.by import By
from pages.base_page import BasePage
class LoginPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h2")
    EMAIL_FORM = (By.CSS_SELECTOR, "form[action='/auth/email']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "form[action='/auth/email'] button[type='submit']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "form[action='/auth/email'] input[type='email']")

    def load(self, base_url):
        self.open(f"{base_url}/login")
        self.find_element(self.HEADING)
        return self

    def is_loaded(self):
        return self.is_element_present(self.HEADING)

    def get_heading_text(self):
        return self.get_element_text(self.HEADING)

    def reveal_email_input(self):
        self.click_element(self.SUBMIT_BUTTON)
        self.find_element(self.EMAIL_INPUT)
        return self

    def type_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def submit(self):
        self.click_element(self.SUBMIT_BUTTON)

    def login_with_email(self, email):
        self.reveal_email_input()
        self.type_email(email)
        self.submit()

    def get_email_input_validity(self):
        element = self.driver.find_element(*self.EMAIL_INPUT)
        return self.driver.execute_script(
            "return arguments[0].checkValidity();", element
        )