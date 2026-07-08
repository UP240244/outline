import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    driver_instance.quit()
