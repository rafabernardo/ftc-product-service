from core.exceptions.commons_exceptions import NoDocumentsFoundException
from db.mongodb.interfaces.product import ProductsRepositoryInterface
from models.product import Product


class ProductService:
    def __init__(self, repository: ProductsRepositoryInterface):
        self.repository = repository

    def register_product(self, product: Product) -> Product:
        new_product = self.repository.add(product)

        return new_product

    def list_products(
        self, filter_prod: dict, page: int, page_size: int
    ) -> list[Product]:
        paginated_orders = self.repository.list_entities(
            filter_params=filter_prod, page=page, page_size=page_size
        )
        return paginated_orders

    def get_product_by_id(self, product_id: str) -> Product | None:
        product = self.repository.get_by_id(product_id)
        return product

    def count_products(self, filter_prod: dict) -> int:
        total_products = self.repository.count_entities(
            filter_params=filter_prod
        )
        return total_products

    def delete_product(self, product_id: str) -> bool:
        product_exists = self.repository.exists_by_id(product_id)
        if not product_exists:
            raise NoDocumentsFoundException()

        return self.repository.delete_entity(product_id)

    def update_product(self, product_id: str, **kwargs) -> Product:
        product = self.repository.exists_by_id(product_id)
        if not product:
            raise NoDocumentsFoundException()
        return self.repository.update_entity(product_id, **kwargs)
