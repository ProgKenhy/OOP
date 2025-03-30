from abc import ABC, abstractmethod

class Filter(ABC):
    @abstractmethod
    def match(self, message: str) -> bool:
        pass


class SimpleFilter(Filter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, message: str) -> bool:
        return self.pattern in message