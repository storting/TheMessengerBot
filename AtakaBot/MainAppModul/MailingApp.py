import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import os
import sys
import SupportAppModule.SendMessage as SendMessage
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATAbASE_DIR = resource_path('DataBase')

class mailingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Информация по датам и рассылка")
        self.result_text = tk.Text(self, height=40, width=50)
        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса."""
        label_start = tk.Label(self, text="Начальная дата:")
        self.entry_start = tk.Entry(self)
        self.entry_start.insert(0, "01/01/2022")
        label_end = tk.Label(self, text="Конечная дата:")
        self.entry_end = tk.Entry(self)
        self.entry_end.insert(0, "01/01/2022")
        button_process = tk.Button(self, text="Разослать", command=self.process_dates)

        # Расположение элементов
        label_start.grid(row=0, column=0, sticky="w")
        self.entry_start.grid(row=0, column=1)
        label_end.grid(row=1, column=0, sticky="w")
        self.entry_end.grid(row=1, column=1)
        button_process.grid(row=2, columnspan=2)
        self.result_text.grid(row=3, columnspan=2)

    def process_dates(self):
        SendMessage.DriverHandler.open()
        """Обработка вводимых дат и отправка сообщений."""
        # Получаем введённые даты
        start_date_str = self.entry_start.get()
        end_date_str = self.entry_end.get()
        
        # Проверка правильности ввода
        if not start_date_str or not end_date_str:
            messagebox.showwarning("Ошибка", "Необходимо ввести обе даты!")
            return
        
        # Преобразование дат
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты. Используйте dd/mm/yyyy")
            return
        
        # Обработка диапазона дат
        current_date = start_date
        while current_date <= end_date:
            date_to_find = current_date.strftime("%d/%m/%Y")
            
            # Читаем файл и ищем соответствующую дату
            found_data = self.search_data(date_to_find)
            
            # Формирование и вывод результатов
            if found_data:
                self.result_text.insert(tk.END, f"\nИнформация по дате {date_to_find}:\n")
                for first_name, second_name, phone_number in found_data:
                    SendMessage.MessageSend.send_whatsapp_message(phone_number, str(first_name), str(second_name))
                    self.result_text.insert(tk.END, f"{first_name} {second_name}, Телефон: {phone_number}\n")
            else:
                self.result_text.insert(tk.END, f"Нет данных по дате {date_to_find}.\n")
            
            # Переходим к следующему дню
            current_date += timedelta(days=1)
        SendMessage.DriverHandler.close()

    def search_data(self, target_date):
        """Поиск данных по заданной дате."""
        found_data = []
        with open(DATAbASE_DIR, encoding='utf-8') as file:
            for line in file:
                data_list = eval(line.strip())
                if len(data_list) >= 5 and data_list[0].strip() == target_date:
                    found_data.append((data_list[1], data_list[2], data_list[4]))
        return found_data

if __name__ == "__main__":
    processor = mailingApp()
    processor.mainloop()