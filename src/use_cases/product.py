from dependency_injector.wiring import Provide, inject

from interfaces.gateaway import ProductsGatewayInterface
from models.product import Product


class ProductUseCases:
    @inject
    def __init__(
        self,
        product_gateway: ProductsGatewayInterface = Provide[
            ProductsGatewayInterface
        ],
    ):
        self.product_gateway: ProductsGatewayInterface = product_gateway

    def list_products(
        self, filters: dict, page: int, page_size: int
    ) -> list[Product]:
        products = self.product_gateway.list_products(
            filters=filters,
            page=page,
            page_size=page_size,
        )
        return products

    def get_total_products(self, filters: dict) -> int:
        return self.product_gateway.count_products(filters=filters)
