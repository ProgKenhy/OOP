from abc import ABC, abstractmethod
from typing import List
from handlers import Handler
from filters import Filter


class Logger:
    def __init__(self, handlers: List[Handler], filters: List[Filter]) -> None:
        self.handlers = handlers
        self.filters = filters

    def write(self, message: str) -> None:
        if all(filter_ptn for filter_ptn in self.filters):
            for handler in self.handlers:
                handler.handle(message)
