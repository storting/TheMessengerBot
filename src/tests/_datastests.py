import inspect
import importlib.util

try:
    trees_module = importlib.import_module("importlib_resources.trees")
except ModuleNotFoundError:
    print("Модуль importlib_resources.trees не существует.")
else:
    print("Modules imported by importlib_resources.trees:")
    for name, obj in inspect.getmembers(trees_module):
        if inspect.ismodule(obj):
            print(name)