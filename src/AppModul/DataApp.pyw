from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os, sys, codecs, os.path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

TOKEN_DIR = resource_path(r'_internal\Datas\TOKEN\token.json')
CREDENTIALS_DIR = resource_path(r'_internal\Datas\TOKEN\credentials.json')
DATAbASE_DIR = resource_path(r'_internal\Datas\DataBase')

class dataApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("База данных")
        self.geometry("1200x600")
        self.creds = None
        self.values = []
        self.create_widgets()
        self.load_saved_data()

    def create_widgets(self):
        """Создание компонентов Tkinter."""
        label_frame = tk.LabelFrame(self, text="Загрузка данных из Google Таблицы", font=("Arial", 12))
        label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_text_log = scrolledtext.ScrolledText(wrap=tk.WORD, state=tk.DISABLED, bg="#FFFFFF", fg="#333", font=("Helvetica", 8), width=50)
        self.output_text_log.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.SE)
        
        self.entry_ID_google_tabs = tk.Entry(self, width=100)
        self.entry_ID_google_tabs.insert(0, "https://docs.google.com/spreadsheets/d/116w9l5Uwar_ve0J5J92UG4ByaQZsjvJr8fLq8wGsJMo/edit?gid=0#gid=0")
        self.entry_ID_google_tabs.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        self.label_ID_google_tabs = tk.Label(self, text="Введите сслыку на таблицу:")
        self.label_ID_google_tabs.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        button_load = tk.Button(label_frame, text="Обновить данные", command=self.fetch_spreadsheet_data, font=("Arial", 10))
        button_load.pack(side=tk.RIGHT, anchor=tk.SE, padx=10, pady=10)

        self.output_text = scrolledtext.ScrolledText(label_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#F5F5F5", fg="#333", font=("Helvetica", 10))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def load_saved_data(self):
        if os.path.exists(resource_path('DataBase')):
            with codecs.open(resource_path('DataBase'), 'r', encoding='utf-8') as file:
                saved_data = file.readlines()
                if saved_data:
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.delete(1.0, tk.END)
                    for row in saved_data:
                        self.output_text.insert(tk.END, row.strip('\n') + '\n\n')
                    self.output_text.config(state=tk.DISABLED)
                else:
                    self.fetch_spreadsheet_data()
        else:
            self.fetch_spreadsheet_data()

    def fetch_spreadsheet_data(self):
        try:
            if os.path.exists(TOKEN_DIR):
                self.creds = Credentials.from_authorized_user_file(TOKEN_DIR, SCOPES)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_DIR, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                    
                with open(TOKEN_DIR, 'w') as token:
                    token.write(self.creds.to_json())

            service = build('sheets', 'v4', credentials=self.creds)

            try:
                SAMPLE_SPREADSHEET_ID = self.extract_id()
            except:
                messagebox.showerror("Ошибка ввода ссылки", "Необходимо ввести ссылку на таблицу")
            
            SAMPLE_RANGE_NAME = 'Лист1!A2:N3177'

            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
            self.values = result.get('values', [])

            with codecs.open(DATAbASE_DIR, 'w', encoding='utf-8') as file:
                for row in self.values:
                    if len(row) > 13 and row[13]:  
                        filtered_row = row[:9] + row[11:]
                        file.write(str(filtered_row) + "\n")

            self.display_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def display_data(self):
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
                    self.output_text.insert(tk.END, f'{filtered_row}\n\n')
            self.output_text.config(state=tk.DISABLED)
            self.loging_insert()

    def loging_insert(self):
        now = datetime.now()
        formatted_time = now.strftime("%d.%m %H:%M:%S")
        self.output_text_log.config(state=tk.NORMAL)
        self.output_text_log.insert(tk.END, f'Data upload successful!\n \t{formatted_time}\n')
        self.output_text_log.config(state=tk.DISABLED)

    def extract_id(self):
        url = self.entry_ID_google_tabs.get() 
        parts = url.split('/')
        id_part = parts[5]
        return id_part

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

if __name__ == "__main__":
    root = dataApp()
    root.iconbitmap(resource_path(r'_internal\icon.ico'))
    root.mainloop()