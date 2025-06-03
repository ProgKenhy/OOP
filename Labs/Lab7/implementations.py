from typing import List

from interfaces import ILogger, IDataService, INotificationService


class DebugLogger(ILogger):
    def __init__(self, prefix: str = "[DEBUG]"):
        self.prefix = prefix
        print(f"Создан DebugLogger с префиксом: {prefix}")

    def log(self, message: str) -> None:
        print(f"{self.prefix} {message}")


class ReleaseLogger(ILogger):
    def __init__(self, log_level: str = "INFO"):
        self.log_level = log_level
        print(f"Создан ReleaseLogger с уровнем: {log_level}")

    def log(self, message: str) -> None:
        print(f"[{self.log_level}] {message}")


class DebugDataService(IDataService):
    def __init__(self, logger: ILogger, connection_string: str = "debug_db"):
        self.logger = logger
        self.connection_string = connection_string
        self.data = ["debug_item1", "debug_item2"]
        self.logger.log(f"DebugDataService инициализирован с БД: {connection_string}")

    def get_data(self) -> List[str]:
        self.logger.log("Получение данных из debug базы")
        return self.data.copy()

    def save_data(self, data: str) -> bool:
        self.logger.log(f"Сохранение в debug базу: {data}")
        self.data.append(data)
        return True


class ReleaseDataService(IDataService):
    def __init__(self, logger: ILogger, connection_string: str = "prod_db"):
        self.logger = logger
        self.connection_string = connection_string
        self.data = ["prod_item1", "prod_item2", "prod_item3"]
        self.logger.log(f"ReleaseDataService инициализирован с БД: {connection_string}")

    def get_data(self) -> List[str]:
        self.logger.log("Получение данных из производственной базы")
        return self.data.copy()

    def save_data(self, data: str) -> bool:
        self.logger.log(f"Сохранение в производственную базу: {data}")
        self.data.append(data)
        return True


class DebugNotificationService(INotificationService):
    def __init__(self, logger: ILogger, data_service: IDataService):
        self.logger = logger
        self.data_service = data_service
        self.logger.log("DebugNotificationService инициализирован")

    def send_notification(self, recipient: str, message: str) -> bool:
        self.logger.log(f"[DEBUG] Отправка уведомления {recipient}: {message}")
        self.data_service.save_data(f"notification_to_{recipient}")
        return True


class ReleaseNotificationService(INotificationService):
    def __init__(self, logger: ILogger, data_service: IDataService, smtp_server: str = "smtp.example.com"):
        self.logger = logger
        self.data_service = data_service
        self.smtp_server = smtp_server
        self.logger.log(f"ReleaseNotificationService инициализирован с SMTP: {smtp_server}")

    def send_notification(self, recipient: str, message: str) -> bool:
        self.logger.log(f"Отправка email уведомления {recipient}: {message}")
        self.data_service.save_data(f"email_sent_to_{recipient}")
        return True
