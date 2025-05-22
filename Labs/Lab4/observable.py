from typing import Any

from listeners import IPropertyChangedListener, IPropertyChangingListener
from notifications import INotifyDataChanged, INotifyDataChanging


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
