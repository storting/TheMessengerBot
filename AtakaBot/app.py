import os
import threading
import sys
import time
from ctypes import windll

def run_script(script):
    os.system(f'python {script}')

def resource_path(relative_path):
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def activate_window(hwnd):
    """
    Активирует окно, делая его передним фоном.
    :param hwnd: дескриптор окна
    """
    windll.user32.SetForegroundWindow(hwnd)

# Функция для проверки активности потоков и остановки всего приложения
def check_threads_and_exit():
    threads = [thread1, thread2]
    while any(t.is_alive() for t in threads):
        time.sleep(0.1)
    else:
        print("Finished")
        # Завершаем программу


# Полные пути к файлам
file1_path = resource_path(r'MainAppModul\DataApp.py')
file2_path = resource_path(r'MainAppModul\MailingApp.py')

with open('output.log', 'w') as f:
    # Создаем потоки для выполнения скриптов
    thread1 = threading.Thread(target=run_script, args=(file1_path,))
    thread2 = threading.Thread(target=run_script, args=(file2_path,))
    sys.stdout = f
    sys.stderr = f
    # Запускаем оба потока
    thread1.start()
    thread2.start()

    # Ждем завершения любых потоков
    check_threads_and_exit()
