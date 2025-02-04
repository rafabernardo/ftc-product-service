from abc import ABC, abstractmethod

from models.product import Product


class ProductsGatewayInterface(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        raise NotImplementedError
