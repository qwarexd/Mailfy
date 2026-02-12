from ui.chat_window import ChatWindow
import tkinter as tk
from tkinter import ttk

class ContactListWindow:
    def __init__(self, username, on_chat_open_callback):
        self.window = tk.Toplevel()
        self.window.title(f"Mail.Sex Agent - {username}")
        self.window.geometry("280x600")
        self.window.configure(bg="#C1DCFC")

        self.username = username
        self.on_chat_open_callback = on_chat_open_callback # Сохраняем его
        self.create_widgets()
        print("Auth window initialized")

        

    def create_widgets(self):
        # --- Верхняя панель (Профиль) ---
        top_frame = tk.Frame(self.window, bg="#E1F0FF", height=100, relief="groove", bd=1)
        top_frame.pack(fill="x", side="top")

        # Твой ник
        tk.Label(
            top_frame, text=self.username, 
            font=("Tahoma", 10, "bold"), bg="#E1F0FF", fg="#0055A5"
        ).place(x=10, y=10)

        # Статус (текстом, потом заменим на иконку)
        tk.Label(
            top_frame, text="● В сети", 
            font=("Tahoma", 8), bg="#E1F0FF", fg="green"
        ).place(x=10, y=30)

        # МИКРОБЛОГ (топорный стиль 2000-х)
        tk.Label(top_frame, text="Микроблог:", font=("Tahoma", 7), bg="#E1F0FF").place(x=10, y=55)
        self.blog_entry = tk.Entry(top_frame, font=("Tahoma", 8), bd=1)
        self.blog_entry.insert(0, "шел 3 день как я ебу мснджр")
        self.blog_entry.place(x=10, y=72, width=250)

        # --- Список контактов ---
        # Настройка стиля для Treeview, чтобы убрать лишние рамки
        style = ttk.Style()
        style.configure("Treeview", font=("Tahoma", 9), rowheight=25)
        
        self.tree = ttk.Treeview(self.window, show="tree")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # statass
        self.tree.tag_configure('online', foreground='#00AA00') # Зеленый
        self.tree.tag_configure('offline', foreground='#888888') # Серый


        # Наполняем тестовыми данными
        friends = self.tree.insert("", "end", text="Друзья", open=True)
        self.tree.insert(friends, "end", text="admin", tags=('online',))
        self.tree.insert(friends, "end", text="kpk", tags=('online',))
        
        

        # Цвета для статусов
        self.tree.tag_configure('online', foreground='black')
        self.tree.tag_configure('offline', foreground='gray')

        # Обработка двойного клика для открытия чата
        self.tree.bind("<Double-1>", self.open_chat)

    def open_chat(self, event):
        selection = self.tree.selection()
        if not selection: return

        item = selection[0]
        contact_name = self.tree.item(item, "text")

        if contact_name != "Друзья":
            self.on_chat_open_callback(contact_name)