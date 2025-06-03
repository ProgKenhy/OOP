from abc import ABC, abstractmethod
from typing import List


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class IDataService(ABC):
    @abstractmethod
    def get_data(self) -> List[str]:
        pass

    @abstractmethod
    def save_data(self, data: str) -> bool:
        pass


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, message: str) -> bool:
        pass
