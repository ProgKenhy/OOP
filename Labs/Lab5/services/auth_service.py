import json
import os
from abc import ABC, abstractmethod
from typing import Optional

from models.user import User
from repositories.user_repository import IUserRepository


class IAuthService(ABC):
    @property
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    @property
    @abstractmethod
    def current_user(self) -> Optional[User]:
        pass

    @abstractmethod
    def sign_in(self, user: User) -> None:
        pass

    @abstractmethod
    def sign_out(self) -> None:
        pass


class AuthService(IAuthService):
    SESSION_FILE = 'storage/session.json'

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        self._current_user = None
        self._load_session()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save_session()

    def sign_out(self) -> None:
        self._current_user = None
        self._clear_session()

    def _save_session(self):
        os.makedirs('storage', exist_ok=True)
        if self._current_user:
            with open(self.SESSION_FILE, 'w') as f:
                json.dump({'user_id': self._current_user.id}, f)

    def _load_session(self):
        if os.path.exists(self.SESSION_FILE):
            try:
                with open(self.SESSION_FILE, 'r') as f:
                    session = json.load(f)
                    user = self.user_repo.get_by_id(session['user_id'])
                    if user:
                        self._current_user = user
            except (json.JSONDecodeError, KeyError):
                self._clear_session()

    def _clear_session(self):
        if os.path.exists(self.SESSION_FILE):
            os.remove(self.SESSION_FILE)
