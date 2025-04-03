from typing import List
from handlers import LogHandler
from filters import LogFilter


class Logger:
    def __init__(self, handlers: List[LogHandler], filters: List[LogFilter]) -> None:
        self.handlers = handlers
        self.filters = filters

    def write(self, message: str) -> None:
        if all(filter_ptn for filter_ptn in self.filters):
            for handler in self.handlers:
                handler.handle(message)
