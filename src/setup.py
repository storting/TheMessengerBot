from cx_Freeze import setup, Executable
import os, sys

# Информация о приложении
app_name = "MyApp"
version = "1.0"
description = "BUILD 1//0/0"

# Список файлов, входящих в состав приложения
moduls_to_include = [
    "MainAppModul"
]

include_files = [
    'Datas'
]

# Параметры для создания исполняемого файла
options = {
    "build_exe": {
        "include_files": include_files,
        "includes": moduls_to_include
    }
}

# Конструктор приложения
executables = [
    Executable("App.py")
]

# Основной вызов setup
setup(
    name=app_name,
    version=version,
    description=description,
    options=options,
    executables=executables
)