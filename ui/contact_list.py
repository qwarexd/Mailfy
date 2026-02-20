import tkinter as tk
from tkinter import ttk

class ContactListWindow:
    def __init__(self, username, on_chat_open_callback, settings_callback):
        self.window = tk.Toplevel()
        self.window.title(f"Агент - {username}")
        self.window.geometry("250x600")
        self.window.attributes("-topmost", True)
        self.window.attributes("-topmost", False)

        
        self.username = username
        self.on_chat_open_callback = on_chat_open_callback
        self.settings_callback = settings_callback
        self.online_users = []  # Список тех, кто в сети (приходит от сервера)
        self.all_contacts = ["admin", "kpk", "user123"] 
        
        self.create_widgets()

    def create_widgets(self):

        # верхний докбар
        self.header_frame = tk.Frame(self.window, bg="#E1F0FF", height=100, relief="groove", bd=1)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        

        # nickaname omggmfpfmfpm
        tk.Label(
            self.header_frame, text=self.username, 
            font=("Tahoma", 10, "bold"), bg="#E1F0FF", fg="#0055A5"
        ).place(x=10, y=10)

        # statass aww man
        tk.Label(
            self.header_frame, text="● В сети", 
            font=("Tahoma", 8), bg="#E1F0FF", fg="green"
        ).place(x=10, y=30)

        # microblog
        tk.Label(self.header_frame, text="Микроблог:", font=("Tahoma", 7), bg="#E1F0FF").place(x=10, y=55)
        self.blog_entry = tk.Entry(self.header_frame, font=("Tahoma", 8), bd=1)
        self.blog_entry.insert(0, "фетешистский микроблог")
        self.blog_entry.place(x=10, y=72, width=250)

        self.bottom_frame = tk.Frame(self.window, bg="#d4d0c8", height=30, bd=1, relief="raised")
        self.bottom_frame.pack(side="bottom", fill="x")
        self.bottom_frame.pack_propagate(False)
        # menu omffpgmf
        self.menu_btn = tk.Button(self.bottom_frame, text="Меню", font=("Tahoma", 7, "bold"),
                                  command=self.show_main_menu, relief="raised", bd=2)
        self.menu_btn.pack(side="left", padx=2)




        self.tree = ttk.Treeview(self.window, show="tree")
        self.tree.pack(side="bottom", fill="both", expand=True)



        # status indicator
        self.status_label = tk.Label(self.bottom_frame, text="В сети", fg="green",
                                     bg="#d4d0c8", font=("Tahoma", 7))
        self.status_label.pack(side="left", padx=5)




        # конфигурируем цвета статусов ( скоро away !!! )
        self.tree.tag_configure('online', foreground='#00AA00', font=('Arial', 10, 'bold'))
        self.tree.tag_configure('away', foreground='#FF8C00', font=('Tahoma', 8, 'bold')) # стильно и клева
        self.tree.tag_configure('offline', foreground='#888888')

        self.refresh_tree()
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def refresh_tree(self):
        """Обновление списка без дублирования"""
        # Запоминаем, какие группы были открыты (чтобы не схлопывались при обновлении)
        self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert("", "end", text="Контакты", open=True)

        for name in self.all_contacts:
            if name == self.username: continue

            is_on = name in self.online_users
            tag = 'online' if is_on else 'offline'
            status = " (в сети)" if is_on else " (офлайн)"

            self.tree.insert(root_node, "end", text=f"{name}{status}", tags=(tag,))

    def update_online_status(self, users):
        self.online_users = users
        self.refresh_tree()

    def on_item_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return

        raw_text = self.tree.item(item_id, "text")
        clean_name = raw_text.replace(" (в сети)", "").replace(" (оффлайн)", "").strip()

        if clean_name != "Контакты":
            print(f"[UI DEBUG] open chat with : {clean_name}")
            self.on_chat_open_callback(clean_name)

    def show_main_menu(self):

        self.window.update_idletasks()

        main_menu = tk.Menu(self.window, tearoff=0)

        status_menu = tk.Menu(main_menu, tearoff=0)
        status_menu.add_command(label="В сети", command=lambda: self.change_status("В сети"))
        status_menu.add_command(label="Отошел", command=lambda: self.change_status("Отошел"))
        status_menu.add_separator()
        status_menu.add_command(label="Невидимый", command=lambda: self.change_status("Невидимый"))

        main_menu.add_cascade(label="Статус", menu=status_menu)
        main_menu.add_separator()
        main_menu.add_command(label="Настройки", command=self.settings_callback)
        main_menu.add_command(label="О программе", command=self.show_about)
        main_menu.add_separator()
        main_menu.add_command(label="Выход", command=self.window.quit)


        x = self.menu_btn.winfo_rootx()
        y= self.menu_btn.winfo_rooty()
        main_menu.post(x,y - 107)

    def change_status(self, new_status):
        color = "green" if new_status == "В сети" else "orange"
        if new_status == "Невидимый": color = "gray"
        self.status_label.config(text=f"● {new_status}", fg=color)
        print(f"[status] status changed to : {new_status}")

    def show_about(self):
        from tkinter import messagebox
        messagebox.showinfo("О программе", "MailFy Agent 0.4.0\n \nCreated by qware. Все справа спизжены\n \nGithub.com/qwarexd/mailfy")

    def update_online_list(self, user_list):
        """Обновляет весь список контактов на основе данных от сервера"""
        # Сначала "гасим" всех в оффлайн
        for category in self.tree.get_children():
            for contact_id in self.tree.get_children(category):
                nick = self.tree.item(contact_id, "text").split(" (")[0] # Убираем "(в сети)"
                
                if nick in user_list:
                    self.tree.item(contact_id, text=f"{nick} (в сети)", tags=('online',))
                else:
                    self.tree.item(contact_id, text=f"{nick} (офлайн)", tags=('offline',))
        print(f"[GUI] Список онлайна обновлен: {user_list}")