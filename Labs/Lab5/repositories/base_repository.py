import json
import os
from abc import ABC, abstractmethod
from typing import Sequence, Optional, List, TypeVar, Generic

T = TypeVar('T')


class IDataRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass


class JsonDataRepository(IDataRepository[T]):
    def __init__(self, file_path: str, item_class: type[T]):
        self.file_path = file_path
        self._ensure_file_exists()
        self._item_class = item_class

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: List[dict]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all(self) -> Sequence[T]:
        return [self._dict_to_item(item) for item in self._read_data()]

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._read_data():
            if item['id'] == id:
                return self._dict_to_item(item)
        return None

    def add(self, item: T) -> None:
        data = self._read_data()
        data.append(self._item_to_dict(item))
        self._write_data(data)

    def update(self, item: T) -> None:
        data = self._read_data()
        for i, existing_item in enumerate(data):
            if existing_item['id'] == item.id:
                data[i] = self._item_to_dict(item)
                break
        self._write_data(data)

    def delete(self, item: T) -> None:
        data = self._read_data()
        data = [i for i in data if i['id'] != item.id]
        self._write_data(data)

    def _item_to_dict(self, item: T) -> dict:
        return item.__dict__

    def _dict_to_item(self, data: dict) -> T:
        return self._item_class(**data)
