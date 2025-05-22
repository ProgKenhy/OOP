from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IPropertyChangedListener(ABC, Generic[T]):
    @abstractmethod
    def on_property_changed(self, obj: T, property_name) -> None:
        pass


class INotifyDataChanged(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass


class PublisherChanged(INotifyDataChanged):
    def __init__(self, listeners: list[IPropertyChangedListener]) -> None:
        self._listeners = listeners

    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._listeners.remove(listener)


class IPropertyChangingListener(ABC, Generic[T]):
    @abstractmethod
    def on_property_changing(self, obj: T, property_name, old_value, new_value) -> bool:
        pass


class INotifyDataChanging(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass

    @abstractmethod
    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass


class PublisherChanging(INotifyDataChanging):
    def __init__(self, listeners: list[IPropertyChangingListener]) -> None:
        self._listeners = listeners

    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        self._listeners.append(listener)

    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        self._listeners.remove(listener)


if __name__ == "__main__":
    class LoggerListener(IPropertyChangedListener[PublisherChanged]):
        def on_property_changed(self, obj: T, property_name: str) -> None:
            print(f"{property_name} changed")


    class AgeValidator(IPropertyChangingListener[PublisherChanging]):
        def on_property_changing(self, obj: T, property_name, old_value, new_value) -> bool:
            if property_name == "age" and new_value <= obj.min_age:
                print(f"Возраст должен быть не менее {obj.min_age} лет")
                return False
            return True

    logger = LoggerListener()
    class StoreClient:
        def __init__(self):
            self.__age = 50
            self.min_age = 18


        def ageChange(self, new_age: int, ageValidator=AgeValidator) -> bool:
            if ageValidator.on_property_changing(obj=StoreClient, property_name="age", old_value=self.__age,
                                                 new_value=new_age):
                self.__age = new_age
                logger.on_property_changed(obj=StoreClient, property_name="age")

    Michel = StoreClient()
    Michel.ageChange(12)
    Michel.ageChange(20)

