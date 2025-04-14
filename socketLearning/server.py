import socket
import threading
import os

HOST = "192.168.0.197"
PORT = 65432
BUFFER_SIZE = 4096
DOWNLOAD_DIR = "server_downloads"


def handle_client(conn, addr):
    print(f"Подключен клиент: {addr}")
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    while True:
        try:
            header = conn.recv(1024).decode('utf-8')
            if not header:
                break

            if header.startswith("FILE:"):
                # Прием файла
                filename = header[5:]
                filesize = int(conn.recv(1024).decode('utf-8'))
                print(f"\nПрием файла: {filename} ({filesize} байт)")

                filepath = os.path.join(DOWNLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        data = conn.recv(BUFFER_SIZE)
                        f.write(data)
                        bytes_received += len(data)

                print(f"Файл сохранен: {filepath}\nВы (сервер): ", end="")
            else:
                # Обычное сообщение
                print(f"\nКлиент: {header}\nВы (сервер): ", end="")

        except (ConnectionResetError, BrokenPipeError):
            print("\nКлиент отключился.")
            break


def send_messages(conn):
    while True:
        user_input = input("Вы (сервер): ")

        if user_input.startswith("/send "):
            # Отправка файла
            filepath = user_input[6:]
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)

                conn.sendall(f"FILE:{filename}".encode('utf-8'))
                conn.sendall(str(filesize).encode('utf-8'))

                with open(filepath, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)

                print(f"Файл {filename} отправлен\nВы (сервер): ", end="")
            else:
                print(f"Файл не найден: {filepath}\nВы (сервер): ", end="")
        else:
            # Обычное сообщение
            try:
                conn.sendall(user_input.encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError):
                print("Не удалось отправить сообщение. Клиент отключился.")
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен и слушает на {HOST}:{PORT}")
    conn, addr = s.accept()

    receive_thread = threading.Thread(target=handle_client, args=(conn, addr))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(conn)
