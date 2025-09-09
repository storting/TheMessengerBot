import os
import sys
import time
import threading
import tkinter as tk
from tkinter.ttk import Progressbar
from queue import Queue
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DependencyInstallerThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.install_finished = False
        self.error_occurred = False

    def run(self):
        current_dir = sys._MEIPASS
        bat_file_path = os.path.join(current_dir, 'installReq.BAT')
        
        if not os.path.exists(bat_file_path):
            print(f"[ERROR]: Батник не найден ({bat_file_path})")
            self.error_occurred = True
            return
        
        try:
            print("[INFO]: Запуск батника...")
            result = subprocess.run([f'{bat_file_path}'], shell=True, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[ERROR]: Произошла ошибка при выполнении батника. Код завершения: {result.returncode}, Output: {result.stdout.strip()}")
                self.error_occurred = True
                return
            
            print("[SUCCESS]: Установка завершена успешно.")
            self.install_finished = True
        
        except subprocess.CalledProcessError as e:
            print(f"[EXCEPTION]: {e}")
            self.error_occurred = True

def show_progress_window(queue):
    window = tk.Tk()
    window.title("Установлятор3000")
    window.geometry("300x80")
    
    label = tk.Label(window, text="Подгружаем магию", font=("Courier New", 12))
    label.pack(pady=(10, 5))
    
    progress_bar = Progressbar(window, orient='horizontal', length=250, mode='indeterminate')
    progress_bar.pack(padx=10, pady=5)
    progress_bar.start()
    
    thread = DependencyInstallerThread(queue)
    thread.start()
    
    def monitor_execution():
        if thread.install_finished:
            progress_bar.stop()
            if thread.error_occurred:
                tk.messagebox.showerror("Ошибка", "Ошибка при установке зависимостей.")
                sys.exit(1)
            else:
                window.destroy()
        else:
            window.after(100, monitor_execution)
    
    monitor_execution()
    window.mainloop()

def run_module(module_path):
    try:
        print(f"[INFO]: Запуск модуля {module_path}.")
        result = subprocess.run(['pythonw', module_path], capture_output=True, text=True)
        if result.returncode != 0:            
            print(f"[ERROR]: Возникла ошибка при запуске модуля {module_path}. Код завершения: {result.returncode}\nOutput:\n{result.stdout}\nErrors:\n{result.stderr}")            
            sys.exit(result.returncode)
    except FileNotFoundError:        
        print(f"[EXCEPTION]: Файл модуля {module_path} не найден.")        
        sys.exit(1)    
    except Exception as e:        
        print(f"[EXCEPTION]: Общая ошибка при запуске модуля {module_path}: {e}")        
        sys.exit(1)

if __name__ == "__main__":
    try:
        log_filename = f"log_.txt"
        log_file = open(log_filename, 'w', encoding='utf-8')
        sys.stdout = log_file
        sys.stderr = log_file
        print("Начинаем запись в файл...")

        q = Queue()
        show_progress_window(q)

        dataapp_path = resource_path('AppModul/DataApp.pyw')
        mailingapp_path = resource_path('AppModul/MailingApp.pyw')
        
        thread1 = threading.Thread(target=run_module, args=(dataapp_path,))
        thread2 = threading.Thread(target=run_module, args=(mailingapp_path,))
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        sys.stdout.flush()
        sys.stderr.flush()
        print("[FINISHED]: Программа успешно завершена.")
    except Exception as e:
        print(f"[CRITICAL ERROR]: {e}")
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        log_file.close()
        print("Запись в файл завершена.")