import socket
import threading
import sys
import tkinter as tk
from ui.auth_window import AuthWindow
from ui.contact_list import ContactListWindow
from ui.chat_window import ChatWindow


# Global objects
client_socket = None
open_chats = {}
root = None
global_open_chat_handler = None



def listen_server():
    while True:
        try:
            if client_socket:
                data = client_socket.recv(1024).decode('utf-8')
                if not data: break

                print(f"[NET DEBUG] Sended: {data}")

                if ":" in data:
                    sender, message = data.split(":", 1)
                    sender = sender.strip()

                    if sender in open_chats:
                        root.after(0, lambda s=sender, m=message: open_chats[s].display_message(s, m))
                    else:
                        print(f"[LOG] Message from {sender}: {message}")
                        root.after(0, lambda s=sender, m=message: auto_open_chat(s, m))
                        print(f"[AUTO] Открываю новое окно для {sender}")
        except: break

                    
def auto_open_chat(sender, message):
    if global_open_chat_handler:
        global_open_chat_handler(sender, silent=True)
        if sender in open_chats:
            open_chats[sender].display_message(sender, message)





def start_app():
    global root, global_open_chat_handler, client_socket

    root = tk.Tk()
    root.withdraw()

    session = {"username": None}

    def login_callback(user):
        session["username"] = user

    auth = AuthWindow(login_callback)
    root.wait_window(auth.window)

    if session["username"]:
        print(f"[logger] login succes: {session['username']}. Connecting to NET...")
    
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 5555))
            client_socket.send(session["username"].encode('utf-8'))
            threading.Thread(target=listen_server, daemon=True).start()
        except Exception as e:
            print(f"[ERROR] NET not found : {e}")

        

        def open_chat_handler(contact_name, silent=False):
            if contact_name in open_chats:
                if not silent:
                    open_chats[contact_name].window.deiconify()
                    open_chats[contact_name].window.focus()
                return

            def send_msg(name, msg):
                if client_socket: client_socket.send(f"{name}:{msg}".encode('utf-8'))

            chat_win = ChatWindow(contact_name, send_msg)
            open_chats[contact_name] = chat_win

            if silent:
                chat_win.window.iconify()


            chat_win.window.protocol("WM_DELETE_WINDOW", lambda: [chat_win.window.destroy(), open_chats.pop(contact_name, None)])

        global_open_chat_handler = open_chat_handler

        contact_list = ContactListWindow(session["username"], open_chat_handler)

        def on_close_app():
            print("[LOG] Closing app...")
            if client_socket:
                client_socket.close()
            root.quit()
            root.destroy()
            sys.exit()

        contact_list.window.protocol("WM_DELETE_WINDOW", on_close_app)

        root.mainloop()
    else:
        root.destroy()
        sys.exit()
        

if __name__ == "__main__":
    start_app()

    if root:
        root.mainloop()