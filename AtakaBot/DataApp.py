from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import codecs
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

class dataApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Просмотрщик Google Таблиц")
        self.geometry("1000x600")  # Устанавливаем размер окна
        self.creds = None
        self.values = []
        self.create_widgets()
        self.load_saved_data()  # Пробуем загрузить данные из файла DataBase

    def create_widgets(self):
        """Создание компонентов Tkinter."""
        label_frame = tk.LabelFrame(self, text="Загрузка данных из Google Таблицы", font=("Arial", 12))
        label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Поле для отображения данных
        self.output_text = scrolledtext.ScrolledText(label_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#F5F5F5", fg="#333", font=("Helvetica", 10))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Кнопка для принудительного обновления данных
        button_load = tk.Button(label_frame, text="Обновить данные", command=self.fetch_spreadsheet_data, font=("Arial", 10))
        button_load.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)
                
        # Поле для ввода сслыки на таблицу
        self.entry_ID_google_tabs = tk.Entry(self, width=100)
        self.entry_ID_google_tabs.insert(0, "https://docs.google.com/spreadsheets/d/116w9l5Uwar_ve0J5J92UG4ByaQZsjvJr8fLq8wGsJMo/edit?gid=0#gid=0")
        self.entry_ID_google_tabs.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        self.label_ID_google_tabs = tk.Label(self, text="Введите сслыку на таблицу:")
        self.label_ID_google_tabs.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

    def load_saved_data(self):
        """Проверяем наличие файла с данными и показываем их, если они есть."""
        if os.path.exists('DataBase'):
            with codecs.open('DataBase', 'r', encoding='utf-8') as file:
                saved_data = file.readlines()
                if saved_data:
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.delete(1.0, tk.END)
                    for row in saved_data:
                        self.output_text.insert(tk.END, row.strip('\n') + '\n\n')
                    self.output_text.config(state=tk.DISABLED)
                else:
                    self.fetch_spreadsheet_data()  # Нет данных в файле, загружаем свежую порцию
        else:
            self.fetch_spreadsheet_data()  # Файл не найден, значит нужно получить данные из сети

    def fetch_spreadsheet_data(self):
        """Метод для загрузки данных из Google Таблицы."""
        try:
            # Файл токенов хранится локально и используется повторно
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
            # Если токены устарели или отсутствуют
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                    
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())

            service = build('sheets', 'v4', credentials=self.creds)

            # ID таблицы (из URL Гугл-документа)
            try:
                SAMPLE_SPREADSHEET_ID = self.extract_id()
            except:
                messagebox.showerror("Ошибка ввода ссылки", "Необходимо ввести ссылку на таблицу")
            
            # Диапазон чтения (например, лист A1:C10)
            SAMPLE_RANGE_NAME = 'Лист1!A2:N3177'

            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
            self.values = result.get('values', [])

            # Сохраняем данные в файл
            with codecs.open('DataBase', 'w', encoding='utf-8') as file:
                for row in self.values:
                    if len(row) > 13 and row[13]:  
                        filtered_row = row[:9] + row[11:]
                        file.write(str(filtered_row) + "\n")

            self.display_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))  # Сообщаем пользователю о возникшей ошибке

    def display_data(self):
        """Метод для отображения полученных данных в интерфейсе Tkinter."""
        if not self.values:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, 'Данные не найдены.')
            self.output_text.config(state=tk.DISABLED)
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            for idx, row in enumerate(self.values):
                if len(row) > 13 and row[13]:  
                    filtered_row = row[:9] + row[11:]
                    self.output_text.insert(tk.END, f'{idx}. {filtered_row}\n\n')
            self.output_text.config(state=tk.DISABLED)
            print("Data upload successful")

    def extract_id(self):
        url = self.entry_ID_google_tabs.get() 
        parts = url.split('/')  # Разбиваем ссылку на части по символу '/'
        id_part = parts[5]      # Берём шестой элемент списка (нумерация начинается с нуля)
        return id_part          # Возвращаем извлечённый ID

# Список разрешений
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

if __name__ == "__main__":
    app = dataApp()  # Создаём экземпляр класса
    app.mainloop()  # Запускаем цикл обработки событий Tkinter