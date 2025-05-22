from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

T = TypeVar('T')


class IPropertyChangedListener(ABC, Generic[T]):
    @abstractmethod
    def on_property_changed(self, obj: T, property_name: str) -> None:
        pass


class INotifyDataChanged(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass


class NotifiableObject(INotifyDataChanged):
    def __init__(self) -> None:
        self._changed_listeners: list[IPropertyChangedListener] = []

    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        if listener not in self._changed_listeners:
            self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        if listener in self._changed_listeners:
            self._changed_listeners.remove(listener)

    def notify_property_changed(self, property_name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)


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


class ValidatableObject(INotifyDataChanging):
    def __init__(self) -> None:
        self._changing_listeners: list[IPropertyChangingListener] = []

    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        if listener not in self._changing_listeners:
            self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        if listener in self._changing_listeners:
            self._changing_listeners.remove(listener)

    def notify_property_changing(self, property_name: str, old_value: Any, new_value: Any) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True


class ObservableObject(NotifiableObject, ValidatableObject):
    def __init__(self) -> None:
        NotifiableObject.__init__(self)
        ValidatableObject.__init__(self)

    def set_property(self, property_name: str, new_value: Any) -> bool:
        if hasattr(self, f'_{property_name}'):
            old_value = getattr(self, f'_{property_name}')
        else:
            old_value = None

        if not self.notify_property_changing(property_name, old_value, new_value):
            return False

        setattr(self, f'_{property_name}', new_value)
        self.notify_property_changed(property_name)
        return True


class SimpleProduct(ObservableObject):
    def __init__(self, name: str = "", price: float = 0) -> None:
        super().__init__()
        self._name = name
        self._price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self.set_property('name', value)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        self.set_property('price', value)


class NameLogListener(IPropertyChangedListener[SimpleProduct]):
    def on_property_changed(self, obj: SimpleProduct, property_name: str) -> None:
        if property_name != 'name':
            return None
        print(f"[PRODUCT LOG] Название товара изменено на: {obj.name}")


class PriceLogListener(IPropertyChangedListener[SimpleProduct]):
    def on_property_changed(self, obj: SimpleProduct, property_name: str) -> None:
        if property_name != 'price':
            return None
        print(f"[PRICE UPDATE] Цена товара '{obj.name}' обновлена до {obj.price} руб.")


class PriceRangeValidator(IPropertyChangingListener[SimpleProduct]):
    def __init__(self, min_value: float, max_value: float) -> None:
        self._min_value = min_value
        self._max_value = max_value

    def on_property_changing(self, obj: SimpleProduct, property_name: str, old_value, new_value) -> bool:
        if property_name != 'price':
            return True
        if new_value < self._min_value or new_value > self._max_value:
            print((f"[VALIDATION ERROR] Значение {new_value} "
                   f"не лежит в диапазоне {self._min_value}-{self._max_value}"))
            return False
        return True


class NameValidator(IPropertyChangingListener[SimpleProduct]):
    def on_property_changing(self, obj: SimpleProduct, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name == 'name':
            if not isinstance(new_value, str):
                print(f"[VALIDATION ERROR] Имя должно быть строкой")
                return False
            if len(new_value) < 2:
                print(f"[VALIDATION ERROR] Имя должно содержать минимум 2 символа")
                return False
        return True


if __name__ == "__main__":
    product = SimpleProduct()

    product_name_logger = NameLogListener()
    product_price_logger = PriceLogListener()
    product_name_validator = NameValidator()
    product_price_validator = PriceRangeValidator(min_value=100, max_value=1000)

    product.add_property_changed_listener(product_name_logger)
    product.add_property_changed_listener(product_price_logger)
    product.add_property_changing_listener(product_name_validator)
    product.add_property_changing_listener(product_price_validator)

    product.name = "Вишни"
    product.name = "D"
    product.price = 150.5
    product.price = 10000
    print(product.price)

    product.remove_property_changed_listener(product_price_logger)
    product.remove_property_changing_listener(product_price_validator)
    print("Убрал логер и валидатор к price")

    product.price = 10000
    print(product.price)

