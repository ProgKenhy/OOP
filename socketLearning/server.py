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
            # Сначала получаем тип данных (сообщение или файл)
            data_type = conn.recv(5).decode('utf-8')  # "TEXT:" или "FILE:"

            if data_type == "FILE:":
                # Прием файла
                filename_length = int.from_bytes(conn.recv(4), byteorder='big')
                filename = conn.recv(filename_length).decode('utf-8')
                filesize = int.from_bytes(conn.recv(8), byteorder='big')

                print(f"\nПрием файла: {filename} ({filesize} байт)")

                filepath = os.path.join(DOWNLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        data = conn.recv(min(BUFFER_SIZE, filesize - bytes_received))
                        f.write(data)
                        bytes_received += len(data)

                print(f"Файл сохранен: {filepath}\nВы (сервер): ", end="")
            else:
                # Прием обычного сообщения
                message_length = int.from_bytes(conn.recv(4), byteorder='big')
                message = conn.recv(message_length).decode('utf-8')
                print(f"\nКлиент: {message}\nВы (сервер): ", end="")

        except (ConnectionResetError, BrokenPipeError, UnicodeDecodeError):
            print("\nКлиент отключился или произошла ошибка.")
            break


def send_messages(conn):
    while True:
        try:
            user_input = input("Вы (сервер): ")

            if user_input.startswith("/send "):
                # Отправка файла
                filepath = user_input[6:]
                if os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    filesize = os.path.getsize(filepath)

                    # Отправляем метку файла
                    conn.sendall(b"FILE:")
                    # Отправляем длину имени файла (4 байта)
                    conn.sendall(len(filename.encode('utf-8')).to_bytes(4, byteorder='big'))
                    # Отправляем имя файла
                    conn.sendall(filename.encode('utf-8'))
                    # Отправляем размер файла (8 байт)
                    conn.sendall(filesize.to_bytes(8, byteorder='big'))

                    # Отправляем содержимое файла
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
                # Отправка обычного сообщения
                conn.sendall(b"TEXT:")
                # Отправляем длину сообщения (4 байта)
                conn.sendall(len(user_input.encode('utf-8')).to_bytes(4, byteorder='big'))
                # Отправляем само сообщение
                conn.sendall(user_input.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            print("Не удалось отправить сообщение. Клиент отключился.")
            break
        except KeyboardInterrupt:
            print("\nЗавершение работы сервера...")
            conn.close()
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
