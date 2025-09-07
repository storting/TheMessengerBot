import os, sys, time, threading
from ctypes import windll

def run_script(script):
    os.system(f'python {script}')

def resource_path(relative_path):
    try:
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

def check_threads_and_exit():
    threads = [thread1, thread2]
    while any(t.is_alive() for t in threads):
        time.sleep(0.1)
    else:
        print("Finished")

file1_path = resource_path(r'AppModul\DataApp.py')
file2_path = resource_path(r'AppModul\MailingApp.py')

batIns_file_path = resource_path(r'installReq.BAT')
batUnins_file_path = resource_path(r'uninstallReq.BAT')



if __name__ == "__main__":
    try:

        exit_code = os.system(batIns_file_path)

        if exit_code == 0:
            print("Выполнение успешно завершилось.")
            thread1 = threading.Thread(target=run_script, args=(file1_path,))
            thread2 = threading.Thread(target=run_script, args=(file2_path,))

            thread1.start()
            thread2.start()
        else:
            print(f"Произошла ошибка при выполнении батника, код выхода: {exit_code}")
    except:
        print("Программа не запущена!(")
        input("Нажмите Enter для выхода...")

    # Ждем завершения любых потоков
    check_threads_and_exit()
