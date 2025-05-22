from observable import ObservableObject


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
