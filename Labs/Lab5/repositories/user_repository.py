from typing import Optional
from abc import ABC, abstractmethod
from models.user import User

from .base_repository import JsonDataRepository, IDataRepository


class IUserRepository(IDataRepository[User]):
    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        pass


class UserRepository(JsonDataRepository[User], IUserRepository):
    def __init__(self, file_path: str):
        super().__init__(file_path, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for item in self._read_data():
            if item['login'] == login:
                return self._dict_to_item(item)
        return None
