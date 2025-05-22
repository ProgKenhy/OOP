from models import SimpleProduct
from listeners_impl import NameLogListener, PriceLogListener
from validators import NameValidator, PriceRangeValidator

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
