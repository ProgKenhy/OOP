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
            # Получаем тип данных (5 байт)
            data_type = sock.recv(5).decode('utf-8')

            if data_type == "FILE:":
                # Прием файла
                filename_length = int.from_bytes(sock.recv(4), byteorder='big')
                filename = sock.recv(filename_length).decode('utf-8')
                filesize = int.from_bytes(sock.recv(8), byteorder='big')

                print(f"\nПрием файла: {filename} ({filesize} байт)")

                filepath = os.path.join(DOWNLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        data = sock.recv(min(BUFFER_SIZE, filesize - bytes_received))
                        f.write(data)
                        bytes_received += len(data)

                print(f"Файл сохранен: {filepath}\nВы (клиент): ", end="")
            else:
                # Прием обычного сообщения
                message_length = int.from_bytes(sock.recv(4), byteorder='big')
                message = sock.recv(message_length).decode('utf-8')
                print(f"\nСервер: {message}\nВы (клиент): ", end="")

        except (ConnectionResetError, BrokenPipeError, UnicodeDecodeError):
            print("\nСервер отключился или произошла ошибка.")
            break


def send_messages(sock):
    while True:
        try:
            user_input = input("Вы (клиент): ")

            if user_input.startswith("/send "):
                # Отправка файла
                filepath = user_input[6:]
                if os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    filesize = os.path.getsize(filepath)

                    # Отправляем метку файла
                    sock.sendall(b"FILE:")
                    # Отправляем длину имени файла (4 байта)
                    sock.sendall(len(filename.encode('utf-8')).to_bytes(4, byteorder='big'))
                    # Отправляем имя файла
                    sock.sendall(filename.encode('utf-8'))
                    # Отправляем размер файла (8 байт)
                    sock.sendall(filesize.to_bytes(8, byteorder='big'))

                    # Отправляем содержимое файла
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
                # Отправка обычного сообщения
                sock.sendall(b"TEXT:")
                # Отправляем длину сообщения (4 байта)
                sock.sendall(len(user_input.encode('utf-8')).to_bytes(4, byteorder='big'))
                # Отправляем само сообщение
                sock.sendall(user_input.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            print("Не удалось отправить сообщение. Сервер отключился.")
            break
        except KeyboardInterrupt:
            print("\nЗавершение работы клиента...")
            sock.close()
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Подключено к серверу. Можно отправлять сообщения и файлы (/send путь_к_файлу)")

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(s)
