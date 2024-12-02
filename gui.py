from tkinter import *
from tkinter import ttk
from gui_comand import *
root = Tk()
root.title("MineServerLauncher")
root.geometry("700x500") 
btn = ttk.Button(text="Главное", command=main_button)
btn = ttk.Button(text="Настройки", command=setinks_button)
btn.pack()

root.mainloop()