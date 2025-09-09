import pymorphy3
import re
from rusgenderdetection import get_gender

textEnd = f"""
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

morph = pymorphy3.MorphAnalyzer()

class Message:
    def __init__(self, nameCustumer, nameBirthday):
        self.nameCustumer = nameCustumer
        self.nameBirthday = nameBirthday

    def ProcessingData(self):
        text = f"""Добрый день!☺🌺❤
        
        Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡
        
        Скоро пора переменых и первых шагов!🎈🎊Мы можем помочь этому событию запомнитсья☺🌺
                        """
        self.nameCustumer = self.clean_name(self.nameCustumer)
        self.nameBirthday = self.clean_name(self.nameBirthday)
        if(self.nameCustumer != None and self.is_personal_name(self.nameCustumer)):            
            if(self.nameBirthday != None and self.is_personal_name(self.nameBirthday)):
                self.nameBirthday = self.decline_name(self.nameBirthday)
                if(self.get_gender_name(self.nameBirthday) == 1):
                    text = f"""*{self.nameCustumer.title()}* добрый день!☺🌺❤
                    Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡
                    
                    Не за горами день рождения Вашего сына *{self.nameBirthday.title()}*🎂❤, _вы еще не думали над подарком🎁, как и где будете отмечать?🎈🎊🎉_
                                """
                elif(self.get_gender_name(self.nameBirthday) == 0):
                    text = f"""*{self.nameCustumer.title()}* добрый день!☺🌺❤
                    
                    Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡
                    
                    Не за горами день рождения Вашей дочери *{self.nameBirthday.title()}*🎂❤, _вы еще не думали над подарком🎁, как и где будете отмечать?🎈🎊🎉_
                                """
            else:
                text = f"""
                *{self.nameCustumer.title()}* добрый день!☺🌺❤
                
                Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡
                
                Скоро пора переменых и первых шагов!🎈🎊Мы можем помочь этому событию запомнитсья☺🌺
                            """
        else:
            text = f"""
            Добрый день!☺🌺❤
            
            Вас беспокоит Владислав администратор лазертаг клуба АТАКА 🔫🧨на Троллейной 37🫡
            
            Скоро пора переменых и первых шагов!🎈🎊Мы можем помочь этому событию запомнитсья☺🌺
                        """
        return text
    
    def final_form_massage(self):
        self.final_text = self.ProcessingData() + textEnd
        return self.final_text

    def is_personal_name(self, word):
        parsed_word = morph.parse(word)[0]

        return ('Name' in parsed_word.tag) or False

    def decline_name(self, name):
        cleaned_text = re.sub(r'[^\u0400-\u04FF\s]', '', name)
        butyavka = morph.parse(cleaned_text.strip())[0]
        gent = butyavka.inflect({'gent'})

        return gent.word
    
    def clean_name(self, name):
        cleaned_text = re.sub(r'[^\u0400-\u04FF\s]', '', name)
        return cleaned_text
    
    def get_gender_name(self, name):
        parse_result = morph.parse(name)[0]
        normalForm = parse_result.normal_form
        return get_gender(normalForm)