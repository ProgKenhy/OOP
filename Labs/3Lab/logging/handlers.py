import syslog
from abc import ABC, abstractmethod
import socket
from typing import Optional


class LogHandler(ABC):
    @abstractmethod
    def handle(self, message: str) -> None:
        pass


class FileHandler(LogHandler):
    def __init__(self, filename: str, mode: str = 'a') -> None:
        self.filename = filename
        self.mode = mode

    def handle(self, message: str) -> None:
        with open(self.filename, self.mode, encoding='utf-8') as f:
            f.write(f"{message}\n")

class SocketHandler(LogHandler):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._socket: Optional[socket.socket] = None

    def connect(self) -> None:
        """Устанавливает соединение с сокетом"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

    def handle(self, message: str) -> None:
        """Отправляет сообщение через сокет"""
        if not self._socket:
            self.connect()
        try:
            self._socket.sendall(f"{message}\n".encode('utf-8'))
        except (OSError, socket.error):
            self._socket = None  # Сброс соединения при ошибке
            raise

    def __del__(self) -> None:
        """Закрывает сокет при удалении объекта"""
        if self._socket:
            self._socket.close()

class ConsoleHandler(LogHandler):
    def handle(self, message: str) -> None:
        print(f"[LOG] {message}")

class SyslogHandler(LogHandler):
    def __init__(self, facility: int = syslog.LOG_USER) -> None:
        syslog.openlog(facility=facility)

    def handle(self, message: str) -> None:
        """Записывает сообщение в системный лог"""
        syslog.syslog(message)

