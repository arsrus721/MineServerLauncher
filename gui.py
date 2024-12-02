from tkinter import *
from tkinter import ttk
from api_handler import *
from gui_comand import *
versions = get_minecraft_versions()
def up_button():
    versions = get_minecraft_versions()


root = Tk()
root.title("MineServerLauncher")
root.geometry("700x500") 


btn = ttk.Button(text="Главное", command=main_button)
btn1 = ttk.Button(text="Настройки", command=setinks_button)
btn2 = ttk.Button(text="Обновить", command=up_button)

combobox = ttk.Combobox(root, values=versions)
combobox.pack(anchor=NW, padx=6, pady=6)

btn.place(x=20, y=30)
btn1.pack()
btn2.pack()
root.mainloop()
