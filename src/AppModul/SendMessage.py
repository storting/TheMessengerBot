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
import time, pyperclip, os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from MessageCraft import Message

#ПУТЬ К ПРОФИЛЮ
home_path = str(Path.home())
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
        try:
            link = f'https://web.whatsapp.com/send/?phone={phone_number}'
            driver.get(link)
        except:
            print("Ссылка недействительна" + str(link))
        pyperclip.copy(message)
        try:
            wait = WebDriverWait(driver, 60)
            main_container = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[@id="main"]'))
            )

            # Использование точного селектора для реальных сообщений
            messages_xpath = './/div[@class="x78zum5 xdt5ytf"]'
            message_elements = main_container.find_elements(By.XPATH, messages_xpath)
            if len(message_elements) <= 0:
                print(len(message_elements))
                print("Пустой чат, начинаю отправку сообщения!")
                textbox = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]//footer//div[@contenteditable="true"]')))
                textbox.click()
                textbox.send_keys(Keys.CONTROL, 'v')
                textbox.send_keys("""
                                """)
                time.sleep(2)
                print("Сообщение успешно отправлено!")
            else:
                print("В активном чате уже есть сообщения.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def find_message_history():
        return