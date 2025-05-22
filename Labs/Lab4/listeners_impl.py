from listeners import IPropertyChangedListener
from models import SimpleProduct


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
