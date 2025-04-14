import socket
import threading

HOST = "192.168.0.197"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn, addr):
    print("New connection from", addr)
    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"\nКлиент: {data}\nВы (сервер): ", end="")
        except (ConnectionResetError, BrokenPipeError):
            print("\nConnection lost")
            break


def send_messages(conn):
    while True:
        message = input("Your message: ")
        try:
            conn.sendall(message.encode("utf-8"))
        except (ConnectionResetError, BrokenPipeError):
            print("\nConnection lost")
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()

    receive_thread = threading.Thread(target=handle_client, args=(conn, addr))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(conn)
