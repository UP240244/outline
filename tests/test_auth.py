import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("user, pwd, mensaje_esperado", [
    ("invalido@test.com", "12345", "Credenciales incorrectas"),
    ("", "password123", "El campo usuario es obligatorio")
])
def test_login_escenarios_error(driver, user, pwd, mensaje_esperado):
    driver.get("http://localhost:3000/login")
    lp = LoginPage(driver)
    lp.login(user, pwd)
    assert lp.obtener_mensaje_error() == mensaje_esperado

def test_login_exitoso(driver):
    driver.get("http://localhost:3000/login")
    lp = LoginPage(driver)
    lp.login("admin@outline.com", "PasswordSeguro123")
    assert "dashboard" in driver.current_url
