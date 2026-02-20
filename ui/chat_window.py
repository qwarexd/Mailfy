import tkinter as tk
from tkinter import scrolledtext
import ctypes

class ChatWindow:
    def __init__(self, contact_name, send_callback):
        self.window = tk.Toplevel() # Toplevel, чтобы не закрывать список контактов
        self.window.title(f"Разговор с {contact_name} - MailFy Agent")
        self.window.geometry("400x500")
        self.window.configure(bg="#F0F4F9")


        self.send_callback = send_callback
        self.contact_name = contact_name
        self.create_widgets()

    def create_widgets(self):
        # Верхняя панель с именем
        header = tk.Frame(self.window, bg="#E1F0FF", height=40, bd=1, relief="groove")
        header.pack(fill="x")
        tk.Label(header, text=f"Чат с: {self.contact_name}", bg="#E1F0FF", font=("Tahoma", 10, "bold")).pack(pady=10)

        # Область сообщений
        self.chat_history = scrolledtext.ScrolledText(self.window, state='disabled', font=("Tahoma", 9))
        self.chat_history.pack(fill="both", expand=True, padx=5, pady=5)

        # Панель ввода
        input_frame = tk.Frame(self.window, bg="#F0F4F9")
        input_frame.pack(fill="x", side="bottom", padx=5, pady=5)

        self.msg_entry = tk.Entry(input_frame, font=("Tahoma", 10))
        self.msg_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_message()) # Отправка по Enter

        self.send_btn = tk.Button(input_frame, text="Отправить", command=self.send_message, bg="#E1E1E1")
        self.send_btn.pack(side="right", padx=5)

    def send_message(self):
        message = self.msg_entry.get()
        if message:
            self.display_message("Вы", message) # Показываем у себя
            self.send_callback(self.contact_name, message) # Отправляем в сеть
            self.msg_entry.delete(0, tk.END)

    def display_message(self, sender, message):
        self.chat_display.config(state='normal') # Разрешаем редактирование
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled') # Запрещаем обратно
        self.chat_display.see(tk.END) # Прокрутка вниз
        
        if self.window.state() == 'iconic':

            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())
            ctypes.windll.user32.FlashWindow(hwnd, True)