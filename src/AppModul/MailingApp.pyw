import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import os
import sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
import SendMessage as SendMessage
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from rebort import RebortSystem 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATAbASE_DIR = resource_path(r'_internal\Datas\DataBase')

class mailingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Рассыльщик")
        self.result_text = tk.Text(self, height=60, width=50)
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
        button_rebort = tk.Button(self, text="Открыть WA", command=self.open_rebort_system)
        #self.entry_num = tk.Entry(self)
        #self.entry_num.insert(tk.END, "+79137898373")

        label_start.grid(row=0, column=0, sticky="w")
        self.entry_start.grid(row=0, column=1)
        label_end.grid(row=1, column=0, sticky="w")
        self.entry_end.grid(row=1, column=1)
        button_process.grid(row=2, column=0)
        button_rebort.grid(row=2, column=1)
        #self.entry_num.grid(row=3, columnspan=2, padx=3, pady=3)
        self.result_text.grid(row=4, columnspan=2)

    def process_dates(self):
        SendMessage.DriverHandler.open()
        start_date_str = self.entry_start.get()
        end_date_str = self.entry_end.get()
        
        if not start_date_str or not end_date_str:
            messagebox.showwarning("Ошибка", "Необходимо ввести обе даты!")
            return
        
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты. Используйте dd/mm/yyyy")
            return
        
        current_date = start_date
        while current_date <= end_date:
            date_to_find = current_date.strftime("%d/%m/%Y")
            found_data = self.search_data(date_to_find)
            if found_data:
                self.result_text.insert(tk.END, f"\nИнформация по дате {date_to_find}:\n")
                for first_name, second_name, phone_number in found_data:
                    SendMessage.MessageSend.send_whatsapp_message(phone_number, str(first_name), str(second_name))
                    self.result_text.insert(tk.END, f"{first_name} {second_name}, Телефон: {phone_number}\n")
            else:
                self.result_text.insert(tk.END, f"Нет данных по дате {date_to_find}.\n")
            current_date += timedelta(days=1)
        SendMessage.DriverHandler.close()

    def open_rebort_system(self):
        RebortSystem.open()

    def search_data(self, target_date):
        found_data = []
        with open(DATAbASE_DIR, encoding='utf-8') as file:
            for line in file:
                data_list = eval(line.strip())
                if len(data_list) >= 5 and data_list[0].strip() == target_date:
                    found_data.append((data_list[1], data_list[2], data_list[4]))
        return found_data

if __name__ == "__main__":
    root = mailingApp()
    root.iconbitmap(resource_path(r'_internal\icon.ico'))
    root.mainloop()