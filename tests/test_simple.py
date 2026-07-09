from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def test_basico():
    options = Options()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    
    print("Abriendo navegador...")
    driver.get("http://127.0.0.1:3000/login")
    
    # Espera manual para ver qué pasa
    time.sleep(10)
    
    # Imprime qué ve Selenium
    print("URL final: " + driver.current_url)
    print("Título: " + driver.title)
    
    driver.quit()

if __name__ == "__main__":
    test_basico()