import socket
import threading

# Настройки
HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Словарь: { "Ник": сокет }
clients = {}

def handle_client(client_socket, sender_nickname):
    """Обрабатываем сообщения ОТ конкретного клиента"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message: break
            
            print(f"[LOG] {sender_nickname} прислал: '{message}'")
            
            # Протокол: "ПОЛУЧАТЕЛЬ:ТЕКСТ"
            if ":" in message:
                target_name, text = message.split(":", 1)
                
                # Очищаем имя получателя от лишних пробелов
                target_name = target_name.strip()
                
                # ГЛАВНЫЙ МОМЕНТ: Ищем СОКЕТ ПОЛУЧАТЕЛЯ
                if target_name in clients:
                    target_socket = clients[target_name]
                    
                    # Формируем сообщение для получателя: "ОТПРАВИТЕЛЬ:ТЕКСТ"
                    final_msg = f"{sender_nickname}:{text}"
                    
                    # ШЛЕМ ИМЕННО ПОЛУЧАТЕЛЮ!
                    target_socket.send(final_msg.encode('utf-8'))
                    print(f"[--->] Переслано от {sender_nickname} для {target_name}")
                
                else:
                    print(f"[ERROR] Пользователь '{target_name}' не найден в {list(clients.keys())}")
                    # Можно вернуть ошибку отправителю, но пока не будем спамить
            else:
                print(f"[LOG] Странное сообщение (без двоеточия): {message}")
                
        except Exception as e:
            print(f"[ERROR] Ошибка с {sender_nickname}: {e}")
            break
            
    # Если вылетели из цикла — удаляем клиента
    print(f"[LOG] {sender_nickname} отключился")
    if sender_nickname in clients:
        del clients[sender_nickname]
    client_socket.close()

def receive():
    print(f"Сервер запущен на {HOST}:{PORT}...")
    while True:
        try:
            client, address = server.accept()
            print(f"[NEW] Подключение с {str(address)}")

            # 1. Сразу ждем никнейм (первое сообщение)
            nickname = client.recv(1024).decode('utf-8')
            
            # Сохраняем клиента в словарь
            clients[nickname] = client
            
            print(f"[LOGIN] Зарегистрирован: {nickname}")
            print(f"[LIST] Сейчас онлайн: {list(clients.keys())}")
            
            # Запускаем поток для этого клиента
            thread = threading.Thread(target=handle_client, args=(client, nickname))
            thread.start()
        except Exception as e:
            print(f"[CRITICAL] Ошибка при подключении: {e}")

if __name__ == "__main__":
    receive()