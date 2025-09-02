import os
import subprocess
import psutil
from time import sleep
import sys

try:
    # Получаем реальный путь к исполняемому файлу
    EXECUTABLE_PATH = os.path.realpath(sys.executable)
except OSError:
    print("Ошибка определения пути к исполняемому файлу.")
    sys.exit(1)

# Поднимаемся на уровень вверх к родительской директории
PROJECT_DIR = os.path.dirname(EXECUTABLE_PATH)
PROJECT_DIR = os.path.dirname(PROJECT_DIR)

VENV_PATH = os.path.join(PROJECT_DIR, 'venv')  # Предположим, .venv лежит в корневом каталоге проекта

# Определение полного пути к интерпретатору Python в виртуальной среде
PYTHON_EXE = os.path.join(VENV_PATH, 'Scripts', 'python.exe')

# Проверяем наличие интерпретатора Python
if not os.path.isfile(PYTHON_EXE):
    raise FileNotFoundError(f"Файл {PYTHON_EXE} не найден.")

# Создание нового окружения для запуска приложений
new_env = dict(os.environ)
new_env['PATH'] = f"{VENV_PATH}\\Scripts;{os.getenv('PATH')}"  # Обновляем PATH для виртуального окружения

def start_app(file_name):
    p = subprocess.Popen([PYTHON_EXE, file_name], env=new_env)
    return p

def check_process(pid):
    try:
        proc = psutil.Process(pid)
        return proc.is_running()
    except psutil.NoSuchProcess:
        return False

if __name__ == "__main__":
    # Запуск двух приложений в отдельных процессах
    mailing_proc = start_app(f'{PROJECT_DIR}\MailingApp.py')
    data_proc = start_app(f'{PROJECT_DIR}\DataApp.py')

    # Сохраняем PID обоих процессов
    mail_pid = mailing_proc.pid
    data_pid = data_proc.pid

    try:
        while True:
            # Проверяем оба процесса
            if not check_process(mail_pid) or not check_process(data_pid):
                print("Один из процессов завершил свою работу.")
                break
            else:
                sleep(1)  # Пауза перед повторной проверкой
    finally:
        print("Завершаемся...")
        mailing_proc.terminate()
        data_proc.terminate()