from abc import ABC, abstractmethod


class Command(ABC):
    """Базовый интерфейс для всех команд"""

    @abstractmethod
    def execute(self):
        """Выполнить команду"""
        pass

    @abstractmethod
    def undo(self):
        """Отменить команду"""
        pass

    @abstractmethod
    def get_description(self):
        """Получить описание команды для логирования"""
        pass
