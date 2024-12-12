import tkinter as tk
from tkinter import ttk
from config import *

def setinks():
    onlain_var = tk.BooleanVar(value=True)
    pvp_var = tk.BooleanVar(value=True)
    wlist_var = tk.BooleanVar(value=False)
    comand_blok_var = tk.BooleanVar(value=True)

    window = tk.Tk()
    window.title("Новое окно")
    window.geometry("400x500")

    geims_label = ttk.Label(window, text="Режим Игры")
    geims_label.pack()
    geims_combobox = ttk.Combobox(window, values=["Выживание", "Творчество"], state="readonly")
    geims_combobox.pack(pady=5)
    geims_combobox.set("Выживание")

    plaers_label = ttk.Label(window, text="Количество Игроков")
    plaers_label.pack()
    plaers = ttk.Spinbox(window, from_=1, to=1000)
    plaers.set(10)
    plaers.pack()

    # Создаем переменные для Checkbutton
    onlain_mode = ttk.Checkbutton(window, text="Проверка на лицензию", variable=onlain_var)
    onlain_mode.pack()

    side0 = ttk.Label(window, text="Сид мира")
    side0.pack()
    text_area = tk.Text(window, height=1, width=40)
    text_area.pack(pady=10)

    side = ttk.Label(window, text="Порт Мира от 1 до 65535")
    side.pack()
    port_area = ttk.Entry(window, width=6)
    port_area.pack(pady=10)
    port_area.insert(0, "25565")  # Вставляем текст в начало поля

    PVP_mode = ttk.Checkbutton(window, text="PVP", variable=pvp_var)
    PVP_mode.pack()

    wlist_mode = ttk.Checkbutton(window, text="белый лист", variable=wlist_var)
    wlist_mode.pack()

    comand_blok_mode = ttk.Checkbutton(window, text="Включить Командный блок", variable=comand_blok_var)
    comand_blok_mode.pack()

    server = ttk.Label(window, text="Описание сервера")
    server.pack()
    Server_neme = tk.Text(window, height=1, width=45)
    Server_neme.pack(pady=10)

    def sevs():
        write_config('geims', geims_combobox.get())
        write_config('namPlaers', plaers.get())
        write_config('onlainMode', onlain_var.get())
        write_config('Port_server', port_area.get())  # Получаем значение из поля ввода
        write_config('PVPon', pvp_var.get())
        write_config('wlist', wlist_var.get())
        write_config('comand_blok', comand_blok_var.get())

    btn1 = tk.Button(window, text="Сохранить", command=sevs)
    btn1.pack()
    
    window.mainloop()