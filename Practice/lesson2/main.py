from abc import ABC, abstractmethod
from typing import List
from unittest import case


class Logger(ABC):
    @abstractmethod
    def write(self, message: str) -> None:
        pass


class FileLogger(Logger):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write(self, message: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(f"{message}\n")


class ConsoleLogger(Logger):
    def write(self, message: str) -> None:
        print(message)


class SyslogLogger(Logger):
    pass


class SocketLogger(Logger):
    pass

class FilteredLogger(Logger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def write(self, message: str) -> None:
        if self.pattern in message:
            super().write(message)

class FilteredFileLogger(FileLogger):
    pass

class FilteredConsoleLogger(ConsoleLogger):
    pass

class Logger:
    def __init__(self, logger_type: str, filter_pattern: str) -> None:
        self.logger_type = logger_type
        self.filter_pattern = filter_pattern

    def write(self, message: str) -> None:
        match self.logger_type:
            case 'File':
                pass
            case 'Console':
                print(message)
            case _:
                pass

# The best practice of inheritance
class Handler(ABC):
    @abstractmethod
    def handle(self, message: str) -> None:
        pass


class FileHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def handle(self, message: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(f"{message}\n")


class Filter(ABC):
    @abstractmethod
    def match(self, message: str) -> bool:
        pass


class SimpleFilter(Filter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, message: str) -> bool:
        return self.pattern in message

class Logger:
    def __init__(self, handlers: List[Handler], filters: List[Filter]) -> None:
        self.handlers = handlers
        self.filters = filters

    def write(self, message: str) -> None:
        for filter in self.filters:
            if not filter.match(message):
                continue
            for handler in self.handlers:
                handler.handle(message)


