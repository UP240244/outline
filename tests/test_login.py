import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.email_sent_page import EmailSentPage


# ---------------------------------------------------------------------
# Caso válido: la página de login carga correctamente
# ---------------------------------------------------------------------
def test_login_page_carga_correctamente(driver, base_url):
    login_page = LoginPage(driver).load(base_url)

    assert login_page.is_loaded()
    assert "login" in login_page.get_heading_text().lower()


# ---------------------------------------------------------------------
# Caso válido: interacción -> aparece el input de correo
# ---------------------------------------------------------------------
def test_click_continuar_con_email_revela_input(driver, base_url):
    login_page = LoginPage(driver).load(base_url)

    login_page.reveal_email_input()

    assert login_page.is_element_present(login_page.EMAIL_INPUT)


# ---------------------------------------------------------------------
# Caso válido: enviar un correo con formato correcto muestra la
# pantalla de confirmación "Check your email"
# ---------------------------------------------------------------------
def test_enviar_email_valido_muestra_confirmacion(driver, base_url):
    login_page = LoginPage(driver).load(base_url)
    correo = "estudiante.qa@example.com"

    login_page.login_with_email(correo)

    email_sent_page = EmailSentPage(driver)
    assert email_sent_page.is_loaded()
    assert correo in email_sent_page.get_confirmed_email()


# ---------------------------------------------------------------------
# Caso de error: enviar el formulario vacío no debe avanzar
# (el campo es 'required', la app nunca llega a hacer POST)
# ---------------------------------------------------------------------
def test_enviar_email_vacio_no_avanza(driver, base_url):
    login_page = LoginPage(driver).load(base_url)
    login_page.reveal_email_input()

    login_page.submit()

    assert login_page.get_email_input_validity() is False
    assert login_page.is_element_present(login_page.EMAIL_INPUT)


# ---------------------------------------------------------------------
# Caso de error: correo con formato inválido no debe avanzar
# ---------------------------------------------------------------------
def test_enviar_email_con_formato_invalido_no_avanza(driver, base_url):
    login_page = LoginPage(driver).load(base_url)
    login_page.reveal_email_input()

    login_page.type_email("esto-no-es-un-correo")
    login_page.submit()

    assert login_page.get_email_input_validity() is False
    assert login_page.is_element_present(login_page.EMAIL_INPUT)


# ---------------------------------------------------------------------
# Caso de frontera: el botón "Back to login" regresa al estado inicial
# ---------------------------------------------------------------------
def test_regresar_desde_pantalla_de_confirmacion(driver, base_url):
    login_page = LoginPage(driver).load(base_url)
    login_page.login_with_email("otro.usuario@example.com")

    email_sent_page = EmailSentPage(driver)
    assert email_sent_page.is_loaded()

    email_sent_page.go_back_to_login()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(login_page.HEADING)
    )
    assert login_page.is_loaded()


# ---------------------------------------------------------------------
# Prueba data-driven: valida distintos formatos de correo usando la
# validación nativa HTML5 del input (type="email" + required)
# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    "email, es_valido",
    [
        ("nombre.apellido@dominio.com", True),
        ("nombre@subdominio.dominio.mx", True),
        ("sin-arroba-dominio.com", False),
        ("usuario@", False),
        ("", False),
    ],
)
def test_validez_formato_email(driver, base_url, email, es_valido):
    login_page = LoginPage(driver).load(base_url)
    login_page.reveal_email_input()
    login_page.type_email(email)

    assert login_page.get_email_input_validity() is es_valido