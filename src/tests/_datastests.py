import os, sys
import json

def resource_path_buid(relative_path):
    if(input() == 1):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    else:
        base_path = r'C:\Users\stort\Documents\MobileMonsters\TheMessengerBot'
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

def resource_path(relative_path):
    base_path = r'C:\Users\stort\Documents\MobileMonsters\TheMessengerBot'
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)

TOKEN_DIR = resource_path(r'Datas\TOKEN\token.json')
CREDENTIALS_DIR = resource_path(r'Datas\TOKEN\credentials.json')

print(TOKEN_DIR)
print("\n")

with open(TOKEN_DIR, 'r') as file:
    data = json.load(file)
print(data)
