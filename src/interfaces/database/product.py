import abc

from models.product import Product


class ProductsRepositoryInterface(abc.ABC):
    def __init__(self): ...

    @abc.abstractmethod
    def add(self, product: Product) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, id: int) -> Product | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_products(self, filter: dict, page: int, page_size: int) -> list[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def count_products(self, filter: dict) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_product(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def exists_by_id(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def update_product(self, id: int, **kwargs) -> Product:
        raise NotImplementedError
