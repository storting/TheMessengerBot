from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

# Путь к профилю
home_path = str(Path.home())
PROFILE_PATH = Path(home_path, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'AppProfile')


class RebortSystem:
    def open():
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Отключить автоматическое закрытие браузера
        chrome_options.add_argument("--disable-extensions")  # Отключить расширения
        chrome_options.add_argument("--disable-gpu")  # Отключить GPU ускорение
        chrome_options.add_argument("--no-sandbox")  # Отключить песочницу
        chrome_options.add_argument("--disable-dev-shm-usage")  # Отключить использование /dev/shm

        if PROFILE_PATH:
            chrome_options.add_argument(f"--user-data-dir={PROFILE_PATH}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        link = f'https://web.whatsapp.com/'
        driver.get(link)

        wait = WebDriverWait(driver, 60)  # Увеличьте время ожидания до 60 секунд
        textbox = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]//footer//div[@contenteditable="true"]')))