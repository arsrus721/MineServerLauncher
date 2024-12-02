from tkinter import *
import gui_comand
root = Tk()
root.title("MineServerLauncher")
root.geometry("700x500") 
btn = ttk.Button(text="Click Me", command=main_button)
btn.pack()

root.mainloop()