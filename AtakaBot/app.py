import os
import subprocess
import psutil
from time import sleep

# Укажите путь к вашей виртуальной среде
VENV_PATH = r'venv'

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
    mailing_proc = start_app('MailingApp.py')
    data_proc = start_app('DataApp.py')

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