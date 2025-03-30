from abc import ABC, abstractmethod



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