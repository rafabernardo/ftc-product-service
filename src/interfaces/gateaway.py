from abc import ABC

from models.product import Product


class ProductsGatewayInterface(ABC):
    def list_products(self, filters: dict, page: int, page_size: int) -> list[Product]:
        raise NotImplementedError

    def count_products(self, filters: dict) -> int:
        raise NotImplementedError
