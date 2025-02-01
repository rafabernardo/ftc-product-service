from adapters.models.page import Page
from adapters.models.product import PagedProductsOut, ProductOut
from interfaces.database.product import ProductsDatabaseInterface
from interfaces.gateaway import ProductsGatewayInterface
from models.product import Category, Product


class ProductUseCases:
    def __init__(self, product_gateway: ProductsGatewayInterface):
        self.product_gateway: ProductsGatewayInterface = product_gateway

    def list_products(self, filters: dict, page: int, page_size: int) -> list[Product]:
        products = self.product_gateway.list_products(
            filters=filters,
            page=page,
            page_size=page_size,
        )
        return products

    def get_total_products(self, filters: dict) -> int:
        return self.product_gateway.count_products(filters=filters)
