import abc

from models.product import Product


class ProductsDatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self): ...

    @abc.abstractmethod
    def add_product(self, product: Product) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def update_product(self, product: Product, update_set: dict) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_product(self, product_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def list_products(
        self, filters: dict, page: int, page_size: int
    ) -> list[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def count_products(self, filters: dict) -> int:
        raise NotImplementedError
