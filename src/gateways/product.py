from dependency_injector.wiring import Provide, inject

from gateways.utils import prepare_document_to_db, replace_id_key
from interfaces.database.product import ProductsDatabaseInterface
from interfaces.gateway import ProductsGatewayInterface
from models.product import Product


class ProductsGateway(ProductsGatewayInterface):
    @inject
    def __init__(
        self,
        products_database: ProductsDatabaseInterface = Provide[
            ProductsDatabaseInterface
        ],
    ):
        self.products_database = products_database

    def add(self, product: Product) -> Product:
        product_data = product.model_dump()
        product_to_db = prepare_document_to_db(product_data)
        self.products_database.add_product(Product(**product_to_db))
        final_product = replace_id_key(product_to_db)
        return Product(**final_product)
