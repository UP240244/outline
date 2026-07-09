import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.mark.parametrize("user, pwd, esperado", [
    ("valido@mail.com", "Correcto123", "dashboard"),
    ("invalido@mail.com", "wrong", "Credenciales incorrectas"),
    ("", "Password123", "El campo usuario es obligatorio"),
])
def test_login_escenarios(driver, user, pwd, esperado):
    # Paso 1: Ir a la raíz para cargar la sesión/cookies
    driver.get("http://127.0.0.1:3000")
    # Paso 2: Ir a login
    driver.get("http://127.0.0.1:3000/login")
    
    # Espera a que el campo de email aparezca
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    
    lp = LoginPage(driver)
    lp.login(user, pwd)

    if "dashboard" in esperado:
        WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
        assert "dashboard" in driver.current_url
    else:
        assert esperado in lp.obtener_error()