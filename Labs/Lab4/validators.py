from typing import Any

from listeners import IPropertyChangingListener
from models import SimpleProduct


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
