import SendMessege
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def process_dates():
    global result_text
    
    # Получаем введённые даты
    start_date_str = entry_start.get()
    end_date_str = entry_end.get()
    
    # Обрабатываем случай пустых полей
    if not start_date_str or not end_date_str:
        messagebox.showwarning("Ошибка", "Необходимо ввести обе даты!")
        return
    
    # Преобразуем введённые даты в объекты datetime
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Ошибка", "Неправильный формат даты. Используйте dd/mm/yyyy.")
        return
    
    # Очищаем область вывода результата
    result_text.delete('1.0', tk.END)
    
    # Проход по всему диапазону дат
    current_date = start_date
    while current_date <= end_date:
        date_to_find = current_date.strftime("%d/%m/%Y")
        
        # Чтение файла и поиск соответствующей даты
        with open('dataBase', encoding='utf-8') as file:
            found_data = []
            for line in file:
                data_list = eval(line.strip())
                if len(data_list) >= 5 and data_list[0].strip() == date_to_find:
                    found_data.append((data_list[1], data_list[2], data_list[4]))
        
        # Выводим результаты
        if found_data:
            result_text.insert(tk.END, f"\nИнформация по дате {date_to_find}:\n")
            for first_name, second_name, phone_number in found_data:
                SendMessege.send_whatsapp_message("+79139598344", first_name, second_name)
                result_text.insert(tk.END, f"{first_name} {second_name}, Телефон: {phone_number}\n")
        else:
            result_text.insert(tk.END, f"Нет данных по дате {date_to_find}.\n")
        
        # Следующий день
        current_date += timedelta(days=1)

# Создание окна приложения
root = tk.Tk()
root.title("Поиск информации по датам")

# Элементы управления
label_start = tk.Label(root, text="Начальная дата:")
entry_start = tk.Entry(root)
label_end = tk.Label(root, text="Конечная дата:")
entry_end = tk.Entry(root)
button_process = tk.Button(root, text="Получить информацию", command=process_dates)
result_text = tk.Text(root, height=10, width=50)

# Размещение элементов в окне
label_start.grid(row=0, column=0, sticky="w")
entry_start.grid(row=0, column=1)
label_end.grid(row=1, column=0, sticky="w")
entry_end.grid(row=1, column=1)
button_process.grid(row=2, columnspan=2)
result_text.grid(row=3, columnspan=2)

# Запуск главного цикла приложения
root.mainloop()