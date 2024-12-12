import tkinter as tk
from tkinter import ttk, messagebox
from api_handler import *
from config import *
from setinks import*
# Initialize the global variable
ver = None  # Declare and initialize ver

# Command functions
def click(): 
    response = messagebox.askyesno(message="Начать загрузку с последнего выброной версии или выбрать другую")
    if response:  # Check user's response
        print("Пользователь выбрал 'Да'")
        
    else:
        print("Пользователь выбрал 'Нет'")

def append_log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + '\n')
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

versions = get_minecraft_versions()

def up_button():
    versions = get_minecraft_versions()
    append_log("Обновление списка")
    append_log("Последнния Выброноя версия Была")
    append_log(read_config('Ver_Server'))
    vers = read_config('Ver_Server')
    download_server(version=vers)

def setinks_button():
    append_log("Запуск Настройки")
    setinks()

def Start():
    global ver  # Declare ver as a global variable
    if ver: 
        ver = version_combobox.get()
        write_config('Ver_Server', ver)
        append_log(f"Конфиг обновлён на версию: {ver}")
    elif read_config('Ver_Server') is None:
        click()
    else:
        append_log("Выберете версию") 


def Stop():
    append_log("Остовка")

# Interface setup
root = tk.Tk()
root.title("MineServerLauncher")
root.geometry("700x500") 

btn1 = tk.Button(text="Настройки", command=setinks_button)
btn2 = tk.Button(text="Обновить", command=up_button)
btn = tk.Button(text="Запустить", command=Start)
btn3 = tk.Button(text="Стоп", command=Stop)
version_combobox = ttk.Combobox(root, values=versions)
version_combobox.pack(pady=5)
btn1.pack()
btn2.pack()
btn.pack()
btn3.pack()
log_text = tk.Text(root, state=tk.DISABLED, height=10, width=35)
log_text.pack(pady=5)
root.mainloop()
