import tkinter as tk
from tkinter import messagebox

class AuthWindow:
    # создаем окно авторизации
    def __init__(self, on_login_callback):
        self.window = tk.Toplevel()
        self.window.title("MailFy Agent 0.2.0")
        self.window.geometry("300x400")
        self.window.configure(bg="#F0F4F9")
        self.window.resizable(False, False)

        self.on_login_callback = on_login_callback
        self.create_widgets()

    def create_widgets(self):
        # логотип // пока заглушка игрушка хуюшка и тд 
        # я уже красный и тд
        self.logo_label = tk.Label(
            self.window, text="@ MailFy Agent",
            font=("Arial", 18, "bold"), fg="#0055A5", bg="#F0F4F9", pady=20
        )
        self.logo_label.pack

        tk.Label(self.window, text="E-mail:", bg="#F0F4F9", font=("Tahoma", 9)).pack(anchor="w", padx=40)
        self.email_entry = tk.Entry(self.window, width=30)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "admin") # Для удобства тестов

        # 2. Поле ввода E-mail
        tk.Label(self.window, text="E-mail:", bg="#F0F4F9", font=("Tahoma", 9)).pack(anchor="w", padx=40)
        self.email_entry = tk.Entry(self.window, width=30)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "admin") # Для удобства тестов

        # 3. Поле ввода Пароля
        tk.Label(self.window, text="Пароль:", bg="#F0F4F9", font=("Tahoma", 9)).pack(anchor="w", padx=40)
        self.pass_entry = tk.Entry(self.window, width=30, show="*")
        self.pass_entry.pack(pady=5)
        self.pass_entry.insert(0, "1234")

        # 4. Чекбокс "Запомнить пароль" (стиль 5.9)
        self.remember_var = tk.BooleanVar()
        self.check = tk.Checkbutton(
            self.window, text="Запомнить пароль", variable=self.remember_var,
            bg="#F0F4F9", activebackground="#F0F4F9", font=("Tahoma", 8)
        )
        self.check.pack(pady=10)

        # 5. Кнопка Входа
        self.login_btn = tk.Button(
            self.window, text="Войти", width=15, height=1,
            command=self.handle_login, bg="#E1E1E1", relief="raised"
        )
        self.login_btn.pack(pady=20)
    
    def handle_login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        self.on_login_callback(email)
        self.window.destroy()


        print(f"[LOG] Нажата кнопка входа. Данные: {email} / {password}")


        if email and password == "1234":
            print("[LOG] Данные верны, вызываем переход...")
            print(f"Успешный вход: {email}")
            self.window.destroy()
            self.on_login_callback(email)
        else:
            print("[LOG] Ошибка: Неверные данные")
            messagebox.showerror("Ошибка", "Неверный e-mail или пароль!\nПодсказка: а хуй тебе мальчик")

if __name__ == "__main__":
    def start_main_app(user):
        print(f"Переход к списку контактов для {user}")
    
    app = AuthWindow(start_main_app)