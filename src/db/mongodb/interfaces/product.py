import abc

from db.mongodb.interfaces.base import BaseRepositoryInterface
from models.product import Product


class ProductsRepositoryInterface(BaseRepositoryInterface[Product]):
    @abc.abstractmethod
    def add(self, product: Product) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def list_entities(
        self,
        filter_params: dict,
        page: int,
        page_size: int,
    ) -> list[Product]:
        raise NotImplementedError
