import os
import subprocess

# Укажите путь к своей виртуальной среде
VENV_PATH = r'myenv'

# Определение полного пути к интерпретатору Python в виртуальной среде
PYTHON_EXE = os.path.join(VENV_PATH, 'Scripts', 'python.exe')

# Проверяем наличие интерпретатора Python
if not os.path.isfile(PYTHON_EXE):
    raise FileNotFoundError(f"Файл {PYTHON_EXE} не найден.")

# Формирование правильного окружения для запуска
new_env = dict(os.environ)
new_env['PATH'] = f"{VENV_PATH}\Scripts;{os.getenv('PATH')}"

def start_app(file_name):
    """
    Запуск отдельного приложения в отдельном процессе с нужным окружением.
    """
    subprocess.Popen([PYTHON_EXE, file_name], env=new_env)

if __name__ == "__main__":
    # Запуск двух приложений в отдельных процессах
    start_app('MailingApp.py')
    start_app('DataApp.py')