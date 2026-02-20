import socket
import threading
import sys
import tkinter as tk
import os
import winsound
from ui.auth_window import AuthWindow
from ui.contact_list import ContactListWindow
from ui.chat_window import ChatWindow
from ui.config_manager import load_config, save_config
from ui.settings_window import SettingsWindow
from logic.idle_manager import IdleManager

current_config = load_config()



# Global objects
client_socket = None
open_chats = {}
root = None
global_open_chat_handler = None
contact_list_instance = None





def open_settings():
    print("[UI] Open settings window...")
    def handle_save(new_config):
        save_config(new_config)

        global current_config
        current_config.update(new_config)

        print(f"[system] config saved : {current_config}")
    SettingsWindow(current_config, handle_save)



def play_message_sound():
    """функция для проигрывания звука уведомления при входящем msg на твой ~~email~~ client
     ||| пока что багнутая ибо звук проигрывается даже при активном окне я хуй знай что с этим делать"""
    sound_path = os.path.join("resources", "message.wav")
    if os.path.exists(sound_path):
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        print("[LOG] что то сломалось и звук не проигрался хз")
        winsound.MessageBeep



def listen_server():
    """cum on , lets go https://www.youtube.com/watch?v=POb02mjj2zE&list=RDMM&index=27"""
    global contact_list_instance
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("[!] Соединение разорвано сервером")
                break
            
            message = data.decode('utf-8')
            print(f"[DEBUG CLIENT] Получено от сервера: {message}") # КРИТИЧНО ДЛЯ ТЕСТА

            # 1. Список онлайн (при входе)
            if message.startswith("SYSTEM:ONLINE_LIST:"):
                user_list = message.replace("SYSTEM:ONLINE_LIST:", "").split(",")
                if contact_list_instance:
                    root.after(0, lambda: contact_list_instance.update_online_list(user_list))

            # 2. Обновление статуса (AWAY/ONLINE)
            elif message.startswith("SYSTEM:USER_STATUS:"):
                # Формат: SYSTEM:USER_STATUS:nickname:status
                parts = message.split(":")
                if len(parts) >= 4:
                    target_nick = parts[2]
                    status_type = parts[3]
                    print(f"[DEBUG] Меняем статус {target_nick} на {status_type}")
                    if contact_list_instance:
                        root.after(0, lambda: contact_list_instance.update_contact_status(target_nick, status_type))

            elif ":" in data:
                sender, message = data.split(":", 1)
                sender = sender.strip()

                play_message_sound() # пиздец х2 // оно кстати сломано
                # и звук проигрывается даже когда окно с диалогом активно !!!

                if sender in open_chats:
                    root.after(0, lambda s=sender, m=message: open_chats[s].display_message(s, m))
                else:
                    print(f"[LOG] Message from {sender}: {message}")
                    root.after(0, lambda s=sender, m=message: auto_open_chat(s, m))
                    print(f"[AUTO] открытие нового окна для {sender}")
        except: break

                    
def auto_open_chat(sender, message):
    if global_open_chat_handler:
        global_open_chat_handler(sender, silent=True)
        if sender in open_chats:
            open_chats[sender].display_message(sender, message)


# а что здесь ты ожилал увидеть? бубс? нет. 



def start_app():
    global root, global_open_chat_handler, client_socket, contact_list_instance

    root = tk.Tk()
    root.withdraw()


    session = {"username": None}
    def login_callback(user): session["username"] = user

    auth = AuthWindow(login_callback)
    root.wait_window(auth.window)

    if not session["username"]:
        sys.exit()

    def open_chat_handler(contact_name, silent=False):
        if contact_name in open_chats:
            try:
                if open_chats[contact_name].window.winfo_exists():
                    if not silent:
                        open_chats[contact_name].window.deiconify()
                        open_chats[contact_name].window.focus()
                    return
                else:
                    open_chats.pop(contact_name)
            except Exception:
                open_chats.pop(contact_name, None)

        def send_msg(name, msg):
            global client_socket
            if client_socket:
                try:
                    client_socket.send(f"{name}:{msg}".encode('utf-8'))
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    print("[crititcal] connection closed!")
                    client_socket = None

        try:
            chat_win = ChatWindow(contact_name, send_msg)
            open_chats[contact_name] = chat_win

            if silent:
                chat_win.window.iconify()

            def on_close():
                if contact_name in open_chats:
                    open_chats.pop(contact_name)
                chat_win.window.destroy()

            chat_win.window.protocol("WM_DELETE_WINDOW", on_close)
            print(f"[LOG] Window for {contact_name} opened")
        except Exception as e:
            print(f"[error] creating window error: {e}")



    global_open_chat_handler = open_chat_handler


        # connecting to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(20) # пиздец куда столько
        client_socket.connect((current_config["server_ip"], 5555))
        client_socket.settimeout(None)
        client_socket.send(session["username"].encode('utf-8'))

        threading.Thread(target=listen_server, daemon=True).start()
    except Exception as e:
        print(f"[critical] Server is offline : {e}")
        client_socket = None # пиздец

    contact_list_instance = ContactListWindow(session["username"], open_chat_handler, open_settings)

    def go_away():
        if contact_list_instance:
            root.after(0, lambda: contact_list_instance.change_status("Отошел"))
            try:
                client_socket.send("SYSTEM:STATUS:AWAY".encode('utf-8'))
            except: pass
        

    def come_back():
        if contact_list_instance:
            root.after(0, lambda: contact_list_instance.change_status("В сети"))
            try:
                client_socket.send("SYSTEM:STATUS:ONLINE".encode('utf-8'))
            except: pass
            

    idle_tracker = IdleManager(
        root, 
        current_config.get("away_timeout", 300), 
        go_away, 
        come_back
    )
    
    # Запускаем цикл проверки простоя
    idle_tracker.check_idle()

    #root.mainloop() пиздец
 

    def on_close_app():
        """бомжереализация выхода из аппки"""
        root.quit()
        sys.exit()
    contact_list_instance.window.protocol("WM_DELETE_WINDOW", on_close_app)

    root.mainloop()


# хз что это
if __name__ == "__main__":
    start_app()

    if root:
        root.mainloop()