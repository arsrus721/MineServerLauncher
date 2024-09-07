import threading
import subprocess
import os
import requests
import logging
import tkinter as tk
from tkinter import ttk, messagebox

# Настройка логирования
logging.basicConfig(filename='server_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Manager")
        self.process = None  # Для хранения процесса сервера

        # Установка фона
        self.root.configure(bg='#d0d0d0')  # Светло-серый фон

        # Меню настроек
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Настройки", menu=self.settings_menu)
        self.settings_menu.add_command(label="Настройки памяти", command=self.open_memory_settings)

        # Виджеты
        self.version_label = tk.Label(root, text="Выберите версию Minecraft:", bg='#d0d0d0')
        self.version_label.pack(pady=5)

        self.versions = get_minecraft_versions()
        self.version_combobox = ttk.Combobox(root, values=self.versions)
        self.version_combobox.pack(pady=5)

        self.memory_frame = tk.Frame(root, bg='#d0d0d0')
        self.memory_frame.pack(pady=5)

        self.xms_label = tk.Label(self.memory_frame, text="Xms (минимум RAM):", bg='#d0d0d0')
        self.xms_label.pack(side=tk.LEFT)
        self.xms_entry = tk.Entry(self.memory_frame)
        self.xms_entry.pack(side=tk.LEFT)
        self.xms_entry.insert(0, "1024")

        self.xmx_label = tk.Label(self.memory_frame, text="Xmx (максимум RAM):", bg='#d0d0d0')
        self.xmx_label.pack(side=tk.LEFT)
        self.xmx_entry = tk.Entry(self.memory_frame)
        self.xmx_entry.pack(side=tk.LEFT)
        self.xmx_entry.insert(0, "2048")

        self.nogui_var = tk.BooleanVar(value=True)
        self.online_mode_var = tk.BooleanVar(value=True)

        self.nogui_check = tk.Checkbutton(root, text="Без графического интерфейса (nogui)", variable=self.nogui_var, bg='#d0d0d0')
        self.nogui_check.pack(pady=5)

        self.online_mode_check = tk.Checkbutton(root, text="Online mode", variable=self.online_mode_var, bg='#d0d0d0')
        self.online_mode_check.pack(pady=5)

        self.start_button = tk.Button(root, text="Запустить сервер", command=self.start_server)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Остановить сервер", command=self.stop_server)
        self.stop_button.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=5)

        self.log_text = tk.Text(root, state=tk.DISABLED, height=10, width=50)
        self.log_text.pack(pady=5)

    def open_memory_settings(self):
        """Открытие окна настроек памяти"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки памяти")
        settings_window.geometry("300x150")

        # Переменные для хранения настроек
        self.xms_var = tk.StringVar(value="1024")
        self.xmx_var = tk.StringVar(value="2048")

        xms_label = tk.Label(settings_window, text="Xms (минимум RAM):")
        xms_label.pack(pady=5)
        xms_entry = tk.Entry(settings_window, textvariable=self.xms_var)
        xms_entry.pack(pady=5)

        xmx_label = tk.Label(settings_window, text="Xmx (максимум RAM):")
        xmx_label.pack(pady=5)
        xmx_entry = tk.Entry(settings_window, textvariable=self.xmx_var)
        xmx_entry.pack(pady=5)

        save_button = tk.Button(settings_window, text="Сохранить", command=self.save_memory_settings)
        save_button.pack(pady=10)

    def save_memory_settings(self):
        """Сохранение настроек памяти"""
        xms = self.xms_var.get()
        xmx = self.xmx_var.get()
        if xms.isdigit() and xmx.isdigit():
            self.xms_entry.delete(0, tk.END)
            self.xms_entry.insert(0, xms)
            self.xmx_entry.delete(0, tk.END)
            self.xmx_entry.insert(0, xmx)
        else:
            messagebox.showerror("Ошибка", "Неверный формат памяти. Введите числа.")

    def start_server(self):
        version = self.version_combobox.get()
        xms = self.xms_entry.get()
        xmx = self.xmx_entry.get()
        nogui = self.nogui_var.get()
        online_mode = self.online_mode_var.get()

        if not version:
            messagebox.showerror("Ошибка", "Выберите версию сервера!")
            return

        if not (xms.isdigit() and xmx.isdigit()):
            messagebox.showerror("Ошибка", "Неверный формат памяти. Введите числа.")
            return

        self.append_log(f"Запуск сервера версии {version} с Xms={xms} и Xmx={xmx}")

        # Поток для запуска сервера
        server_thread = threading.Thread(target=self.run_server, args=(version, xms, xmx, nogui, online_mode))
        server_thread.start()

    def run_server(self, version, xms, xmx, nogui, online_mode):
        jar_file = f'minecraft_server_{version}.jar'
        
        # Проверка наличия файла, если его нет, скачаем
        if not os.path.exists(jar_file):
            self.append_log(f"Файл сервера {jar_file} не найден, начинаем загрузку.")
            jar_file = self.download_server(version)

        # Автоматическое создание или редактирование файла eula.txt
        self.create_eula()

        command = f'java -Xms{xms}M -Xmx{xmx}M -jar {jar_file}'
        if nogui:
            command += " nogui"
        if not online_mode:
            command += " --online-mode false"

        self.append_log(f"Команда для запуска: {command}")

        try:
            # Запуск сервера и сохранение процесса
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            for line in self.process.stdout:
                self.append_log(line.decode().strip())

            self.process.wait()  # Ожидание завершения процесса
            self.append_log(f"Сервер версии {version} завершил работу.")
        except Exception as e:
            self.append_log(f"Ошибка при запуске сервера: {str(e)}")

    def stop_server(self):
        if self.process:  # если процесс запущен
            self.process.terminate()
            self.append_log("Сервер остановлен.")
            self.process = None
        else:
            self.append_log("Сервер не запущен.")

    def download_server(self, version):
        """Скачиваем сервер Minecraft с прогрессом."""
        version_manifest_url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
        version_info = requests.get(version_manifest_url).json()
        for ver in version_info['versions']:
            if ver['id'] == version:
                version_url = ver['url']
                break
        server_info = requests.get(version_url).json()
        server_url = server_info['downloads']['server']['url']

        # Запускаем скачивание
        self.append_log(f"Начинаем скачивание сервера версии {version}...")
        response = requests.get(server_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        file_name = f'minecraft_server_{version}.jar'
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                downloaded += len(chunk)
                self.progress['value'] = (downloaded / total_size) * 100
                self.root.update_idletasks()

        self.append_log(f"Сервер версии {version} скачан.")
        return file_name

    def create_eula(self):
        """Создаем или редактируем eula.txt для автоматического согласия с EULA"""
        eula_file = 'eula.txt'
        try:
            with open(eula_file, 'w') as file:
                file.write('eula=true\n')
            self.append_log("Файл eula.txt создан с соглашением 'eula=true'.")
        except Exception as e:
            self.append_log(f"Ошибка при создании eula.txt: {str(e)}")

    def append_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)


# Получение списка версий Minecraft
def get_minecraft_versions():
    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    response = requests.get(url)
    data = response.json()
    versions = [version['id'] for version in data['versions']]
    return versions

# Запуск приложения
root = tk.Tk()
app = ServerManagerApp(root)
root.mainloop()
