import socket
import threading

HOST = "192.168.0.197"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"\nСервер: {data}\nВы (клиент): ", end="")
        except (ConnectionResetError, BrokenPipeError):
            print("\nConnection lost")
            break


def send_messages(sock):
    while True:
        message = input("Your message: ")
        try:
            sock.sendall(message.encode("utf-8"))
        except (ConnectionResetError, BrokenPipeError):
            print("\nConnection lost")
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.daemon = True
    receive_thread.start()
    send_messages(s)
