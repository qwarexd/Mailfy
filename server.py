import socket
import threading
import time

# Словарь: { "Ник": сокет }
clients = {}

def broadcast_online_list():
    """рassылает всем список nickames, кто в ass прямо сейчас"""
    online_users = ",".join(clients.keys())
    msg = f"SYSTEM:ONLINE_LIST:{online_users}"
    print(f"[SHUMNIY LOG SERVERA] Рассылка списка : {online_users}")
    for nick, sock in clients.items():
        try:
            sock.send(msg.encode('utf-8'))
        except:
            print(f"[connect error] : failed to parse list for {nick}")



def handle_client(client_socket, sender_nickname):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[debug] message from {sender_nickname} : {message}")

            if message.startswith("SYSTEM:STATUS:"):
                parts = message.split(":")
                if len(parts) >= 3:
                    status_type = parts[3] if len(parts) > 3 else parts[2]

                    broadcast_msg = f"SYSTEM:USER_STATUS:{sender_nickname}:{status_type}"
                    print(f"[status] {sender_nickname} теперь {status_type}")

                    for nick, sock in list(clients.items()):
                        if nick != sender_nickname:
                            try:
                                sock.send(broadcast_msg.encode('utf-8'))
                            except:
                                pass
                continue

            # default messages 
            if ":" in message:
                try:
                    target_name, text = message.split(":", 1)
                    if target_name in clients:
                        clients[target_name].send(f"{sender_nickname}:{text}".encode('utf-8'))
                        print(f"[MSG] {sender_nickname} -> {target_name}")
                except ValueError:
                    print(f"[warn] incorrect format of message from {sender_nickname}")
        except Exception as e:
            print(f"[error] flow error {sender_nickname} : {e}")
            break

    if sender_nickname in clients:
        del clients[sender_nickname]
    print(f"[log] {sender_nickname} disconnected")
    broadcast_online_list()
    client_socket.close()


            

def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()
    print("server started on ... я ебу что ли")
    while True:
        client, addr = server.accept()
        nick = client.recv(1024).decode('utf-8')
        clients[nick] = client
        print(f"[LOGIN] {nick} в сети")

        time.sleep(0.5)
        broadcast_online_list()

        threading.Thread(target=handle_client, args=(client, nick), daemon=True).start()

#recieve()
if __name__ == "__main__":
    receive()