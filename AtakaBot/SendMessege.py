from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rusgenderdetection import get_gender
import pyperclip
import time
import pymorphy3
import re

# Создаем объект морфологического анализа
morph = pymorphy3.MorphAnalyzer()

def is_personal_name(word):
    parsed_word = morph.parse(word)[0]
    return ('Name' in parsed_word.tag) or False

def decline_name(name):
    cleaned_text = re.sub(r'[^\u0400-\u04FF\s]', '', name)
    butyavka = morph.parse(cleaned_text.strip())[0]
    gent = butyavka.inflect({'gent'})
    
    return gent.word

# Путь к профилю
PROFILE_PATH = r'C:/Users/evgen/AppData/Local/Google/Chrome/User Data/AppProfile'

def messageCraft(nameCustumer, nameBirthday):
    if(nameBirthday != None and nameBirthday != ''):
        declineName = decline_name(nameBirthday)
        print(declineName + "\t" + nameBirthday + "\t" + str(get_gender(declineName)))
        if(is_personal_name(declineName) and get_gender(declineName) == 1):
            text = f"""
                *{nameCustumer}* добрый день!☺🌺❤

                Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡

                Не за горами день рождения Вашего сына *{declineName.title()}*🎂❤, _вы еще не думали над подарком🎁, как и где будете отмечать?🎈🎊🎉_

                Готовы взять организацию праздника в наши заботливые и профессиональные руки:
                *-Лазертаг игра,*
                *-Аниматор,*
                *-Фотограф,*
                *-Комната отдыха для празднования,*
                *-Скаладром*
                Приглашаем посетить наш лазертаг клуб!🎯🔫

                Приятный сюрприз, только для Вас *10% скидка* при бронировании игры лазертаг!🔥

                Вместо ~1000 рублей~ 🙅‍♀⛔, цена 2-х часовой программы для вашей группы по старым цена *900рублей* за игрока 🕺🏻🔥 

                Новые сценарии и море эмоций!😍 

                Сайт https://www.ataka154.ru/
                Вк  https://vk.com/ataka_154

                _📌Будем благодарны за обратную связь, планируете в нашем клубе либо уже другие планы_

                PS: Желаю хорошего Вам дня, много улыбок, и счастливых моментов!
                """
            return text
        elif(is_personal_name(declineName) and get_gender(declineName) != 1):
            text = f"""
                *{nameCustumer}* добрый день!☺🌺❤

                Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡

                Не за горами день рождения Вашей дочери *{declineName.title()}*🎂❤, _вы еще не думали над подарком🎁, как и где будете отмечать?🎈🎊🎉_

                Готовы взять организацию праздника в наши заботливые и профессиональные руки:
                *-Лазертаг игра,*
                *-Аниматор,*
                *-Фотограф,*
                *-Комната отдыха для празднования,*
                *-Скаладром*
                Приглашаем посетить наш лазертаг клуб!🎯🔫

                Приятный сюрприз, только для Вас *10% скидка* при бронировании игры лазертаг!🔥

                Вместо ~1000 рублей~ 🙅‍♀⛔, цена 2-х часовой программы для вашей группы по старым цена *900рублей* за игрока 🕺🏻🔥 

                Новые сценарии и море эмоций!😍 

                Сайт https://www.ataka154.ru/
                Вк  https://vk.com/ataka_154

                _📌Будем благодарны за обратную связь, планируете в нашем клубе либо уже другие планы_

                PS: Желаю хорошего Вам дня, много улыбок, и счастливых моментов!
                """
            return text
    else:        
        text = f"""
            *{nameCustumer}* добрый день!☺🌺❤

            Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡

            Пришло время немного отдохнуть и развлечься, в этом мы в этом можем очень помочь!🧨☺
            
            Готовы взять организацию праздника в наши заботливые и профессиональные руки:
            *-Лазертаг игра,*
            *-Аниматор,*
            *-Фотограф,*
            *-Комната отдыха для празднования,*
            *-Скаладром*
            Приглашаем посетить наш лазертаг клуб!🎯🔫

            Приятный сюрприз, только для Вас *10% скидка* при бронировании игры лазертаг!🔥

            Вместо ~1000 рублей~ 🙅‍♀⛔, цена 2-х часовой программы для вашей группы по старым цена *900рублей* за игрока 🕺🏻🔥 

            Новые сценарии и море эмоций!😍 

            Сайт https://www.ataka154.ru/
            Вк  https://vk.com/ataka_154

            _📌Будем благодарны за обратную связь, планируете в нашем клубе либо уже другие планы_

            PS: Желаю хорошего Вам дня, много улыбок, и счастливых моментов!
            """ 
        return text

def driverOpen():
    global chrome_options
    global driver
    # Настроим браузер с указанным профилем
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={PROFILE_PATH}")

    # Устанавливаем драйвер
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

def driverQuit():
    driver.quit()

def send_whatsapp_message(phone_number, name1, name2):
    message = messageCraft(name1, name2)
    # Генерируем ссылку для отправки сообщения
    driver.get(f'https://web.whatsapp.com/send/?phone={phone_number}')
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

