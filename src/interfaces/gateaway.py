from abc import ABC, abstractmethod

from models.product import Product


class ProductsGatewayInterface(ABC):
    @abstractmethod
    def list_products(
        self, filters: dict, page: int, page_size: int
    ) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def count_products(self, filters: dict) -> int:
        raise NotImplementedError
