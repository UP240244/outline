from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Selectores corregidos para Outline
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.error_message = (By.CSS_SELECTOR, "div.error-message") # Ajusta según tu CSS real

    def login(self, email, password):
        if email:
            self.driver.find_element(*self.email_input).send_keys(email)
        if password:
            self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def obtener_error(self):
        return self.driver.find_element(*self.error_message).text