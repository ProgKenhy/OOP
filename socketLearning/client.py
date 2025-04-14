import socket
import threading
import os

HOST = "192.168.0.197"
PORT = 65432
BUFFER_SIZE = 4096
DOWNLOAD_DIR = "client_downloads"


def receive_messages(sock):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    while True:
        try:
            header = sock.recv(1024).decode('utf-8')
            if not header:
                break

            if header.startswith("FILE:"):
                # Прием файла
                filename = header[5:]
                filesize = int(sock.recv(1024).decode('utf-8'))
                print(f"\nПрием файла: {filename} ({filesize} байт)")

                filepath = os.path.join(DOWNLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        data = sock.recv(BUFFER_SIZE)
                        f.write(data)
                        bytes_received += len(data)

                print(f"Файл сохранен: {filepath}\nВы (клиент): ", end="")
            else:
                # Обычное сообщение
                print(f"\nСервер: {header}\nВы (клиент): ", end="")

        except (ConnectionResetError, BrokenPipeError):
            print("\nСервер отключился.")
            break


def send_messages(sock):
    while True:
        user_input = input("Вы (клиент): ")

        if user_input.startswith("/send "):
            # Отправка файла
            filepath = user_input[6:]
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)

                sock.sendall(f"FILE:{filename}".encode('utf-8'))
                sock.sendall(str(filesize).encode('utf-8'))

                with open(filepath, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        sock.sendall(bytes_read)

                print(f"Файл {filename} отправлен\nВы (клиент): ", end="")
            else:
                print(f"Файл не найден: {filepath}\nВы (клиент): ", end="")
        else:
            # Обычное сообщение
            try:
                sock.sendall(user_input.encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError):
                print("Не удалось отправить сообщение. Сервер отключился.")
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Подключено к серверу. Можно отправлять сообщения и файлы (/send путь_к_файлу)")

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(s)
