from cx_Freeze import setup, Executable
import os, sys, re

def extract_package_name(requirement):
    """
    Возвращает чистое имя пакета без версии и сравнительных операторов.
    """
    match = re.match(r'^([^\s=<>]+)', requirement)
    if match:
        return match.group(1).strip('\ufeff')
    else:
        return None

# Функция для безопасной обработки файла
def safe_read_requirements():
    valid_packages = []
    with open('requirements.txt', 'r', encoding='utf-16le') as req_file:
        for line in req_file:
            package = extract_package_name(line.strip())
            if package is not None:
                valid_packages.append(package.lower())
    return valid_packages

# Информация о приложении
app_name = "MyApp"
version = "1.0"
description = "BUILD 1//0/0"

packages = safe_read_requirements()

# Список файлов, входящих в состав приложения
moduls_to_include = [
    'MainAppModul\DataApp.py',
    'MainAppModul\MailingApp.py'
    'MainAppModul\SupportAppModule\MessageCraft.py'
    'MainAppModul\SupportAppModule\SendMessage.py'
]

include_files = [
    '..\Datas',
    ('MainAppModul', 'lib')
]

# Параметры для создания исполняемого файла
options = {
    "build_exe": {
        'packages': packages,
        "include_files": include_files
    }
}

# Конструктор приложения
executables = [
    Executable("src/App.py")
]

# Основной вызов setup
setup(
    name=app_name,
    version=version,
    description=description,
    options=options,
    executables=executables
)