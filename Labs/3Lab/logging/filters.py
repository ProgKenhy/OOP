import re
from abc import ABC, abstractmethod

class LogFilter(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        pass


class SimpleLogFilter(LogFilter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern.lower()

    def match(self, text: str) -> bool:
        return self.pattern in text.lower()


class ReLogFilter(LogFilter):
    def __init__(self, regex: str) -> None:
        self.regex = re.compile(regex)

    def match(self, text: str) -> bool:
        return self.regex.search(text) is not None
