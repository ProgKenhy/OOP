from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

T = TypeVar('T')


class IPropertyChangedListener(ABC, Generic[T]):
    @abstractmethod
    def on_property_changed(self, obj: T, property_name: str) -> None:
        pass


class IPropertyChangingListener(ABC, Generic[T]):
    @abstractmethod
    def on_property_changing(self, obj: T, property_name: str, old_value: Any, new_value: Any) -> bool:
        pass
