import tkinter as tk

fonts = [
    ("Arial", 12),
    ("Times New Roman", 12),
    ("Courier New", 12),
    ("Calibri", 12),
    ("Verdana", 12),
    ("Georgia", 12),
    ("Comic Sans MS", 12),
]

root = tk.Tk()
root.title("Пример разных шрифтов")

for font in fonts:
    label = tk.Label(root, text=f"{font[0]} {font[1]}", font=font)
    label.pack(pady=5)

root.mainloop()