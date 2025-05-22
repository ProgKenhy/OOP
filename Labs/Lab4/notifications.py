from abc import ABC, abstractmethod
from typing import TypeVar

from listeners import IPropertyChangedListener, IPropertyChangingListener

T = TypeVar('T')


class INotifyDataChanged(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass


class INotifyDataChanging(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass

    @abstractmethod
    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass
