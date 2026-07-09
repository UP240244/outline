import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("user, pwd, esperado", [
    ("valido@mail.com", "Correcto123", "dashboard"), # Caso válido
    ("invalido@mail.com", "wrong", "Credenciales incorrectas"), # Caso error
    ("", "Password123", "El campo usuario es obligatorio"), # Caso frontera
    ("admin@mail.com", "", "El campo contraseña es obligatorio"), # Caso frontera
    ("malformado", "123", "Formato de correo inválido") # Caso error
])
def test_login_escenarios(driver, user, pwd, esperado):
    driver.get("http://localhost:3000/login")
    lp = LoginPage(driver)
    lp.login(user, pwd)

    if "dashboard" in esperado:
        assert "dashboard" in driver.current_url
    else:
        assert lp.obtener_error() == esperado
