import tkinter as tk
from gui import MinecraftLauncherApp
from downloading import download_minecraft_version
from api import get_minecraft_versions

def main():
    versions = get_minecraft_versions()

    root = tk.Tk()
    app = MinecraftLauncherApp(root, download_minecraft_version, get_minecraft_versions)
    root.mainloop()

if name == "main":
    main()
