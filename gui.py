import tkinter as tk
from tkinter import ttk, messagebox
from api_handler import *

#comand
def append_log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + '\n')
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

versions = get_minecraft_versions()
def up_button():
    versions = get_minecraft_versions()
    append_log("Обновление списка")

def setinks_button():
    print("25")
    append_log("Запуск Настройки")

def Start():
    ver = version_combobox.get()
    if not ver:
        append_log("Выберети Версию")
    else:
        append_log("Скачевание {ver}")

#comand

#Interfes
root = tk.Tk()
root.title("MineServerLauncher")
root.geometry("700x500") 

btn1 = tk.Button(text="Настройки", command=setinks_button)
btn2 = tk.Button(text="Обновить", command=up_button)
btn = tk.Button(text="Запустить", command=Start)
version_combobox = ttk.Combobox(root, values=versions)
version_combobox.pack(pady=5)
btn1.pack()
btn2.pack()
btn.pack()
log_text = tk.Text(root, state=tk.DISABLED, height=10, width=35)
log_text.pack(pady=5)
root.mainloop()
#Interfes