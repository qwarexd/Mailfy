import tkinter as tk

class SettingsWindow:
    def __init__(self, current_config, on_save_callback):
        self.window = tk.Toplevel()
        self.window.title("Настройки Агента")
        self.window.geometry("300x250")
        self.window.resizable(False, False)
        
        self.on_save_callback = on_save_callback

        # Фон как в старых окнах
        self.window.configure(bg="#D4D0C8")

        tk.Label(self.window, text="Настройки подключения", font=("Tahoma", 8, "bold"), bg="#D4D0C8").pack(pady=10)

        # Поле IP
        tk.Label(self.window, text="IP сервера:", bg="#D4D0C8", font=("Tahoma", 8)).pack()
        self.ip_entry = tk.Entry(self.window, font=("Tahoma", 8))
        self.ip_entry.insert(0, current_config["server_ip"])
        self.ip_entry.pack(pady=5)

        # Поле Таймаута
        tk.Label(self.window, text="Таймаут AFK (сек):", bg="#D4D0C8", font=("Tahoma", 8)).pack()
        self.timeout_entry = tk.Entry(self.window, font=("Tahoma", 8))
        self.timeout_entry.insert(0, str(current_config["away_timeout"]))
        self.timeout_entry.pack(pady=5)

        # Кнопка сохранить
        btn_frame = tk.Frame(self.window, bg="#D4D0C8")
        btn_frame.pack(side="bottom", fill="x", pady=15)

        tk.Button(btn_frame, text="OK", width=10, command=self.save, font=("Tahoma", 8)).pack(side="right", padx=10)
        tk.Button(btn_frame, text="Отмена", width=10, command=self.window.destroy, font=("Tahoma", 8)).pack(side="right")

    def save(self):
        try:
            new_cfg = {
                "server_ip": self.ip_entry.get(),
                "away_timeout": int(self.timeout_entry.get())
            }
            self.on_save_callback(new_cfg)
            self.window.destroy()
        except ValueError:
            print("[ERROR] В таймауте должно быть число!")