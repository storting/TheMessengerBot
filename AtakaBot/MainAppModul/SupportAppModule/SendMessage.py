from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import pyperclip
import time
from SupportAppModule.MessageCraft import Message

# ПУТЬ К ПРОФИЛЮ
# Получаем домашний каталог текущего пользователя
home_path = str(Path.home())

# Формируем универсальный путь к User Data в Chrome
PROFILE_PATH = Path(home_path, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'AppProfile')

class DriverHandler: 
    def open():
        global driver

        chrome_options = Options()
        if PROFILE_PATH:
            chrome_options.add_argument(f"--user-data-dir={PROFILE_PATH}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def close():
        if driver:
            driver.quit()

class MessageSend:
    def send_whatsapp_message(phone_number, name1, name2):
        message = Message(name1, name2).final_form_massage()
        # Генерируем ссылку для отправки сообщения
        try:
            link = f'https://web.whatsapp.com/send/?phone={phone_number}'
            driver.get(link)
        except:
            print("Ссылка недействительна" + str(link))
        pyperclip.copy(message)
        try:
            wait = WebDriverWait(driver, 60)
            # Контейнер для ввода сообщения
            textbox = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]//footer//div[@contenteditable="true"]')))
            
            # Щелкаем по полю ввода
            textbox.click()
            
            # Вставляем содержимое буфера обмена
            textbox.send_keys(Keys.CONTROL, 'v')
            
            # Ждём кнопку отправки и нажимаем её
            #send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]//button[@class="_4sWnG"]')))  # Класс кнопки отправки может меняться
            #send_button.click()
            textbox.send_keys("""
                            """)
            time.sleep(2)
            print("Сообщение успешно отправлено!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

