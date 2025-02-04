from bson import ObjectId

from external.mongodb.connection import get_mongo_database
from interfaces.database.product import ProductsDatabaseInterface
from models.product import Product


class ProductMongoRepository(ProductsDatabaseInterface):
    def __init__(self):
        self.database = get_mongo_database()
        self.collection = self.database["Products"]

    def add_product(self, product: Product) -> str:
        result = self.collection.insert_one(product)
        return str(result.inserted_id)

    def update_product(self, product: Product, update_set: dict) -> dict:
        id_filter = self.get_product_by_id_query(product_id=product.id)
        updated_product = self.collection.find_one_and_update(
            id_filter,
            update_set,
            return_document=True,
        )
        return updated_product

    def delete_product(self, product_id: str) -> bool:
        query = self.get_product_by_id_query(product_id=product_id)
        result = self.collection.delete_one(query)
        was_user_deleted = result.deleted_count > 0
        return was_user_deleted

    def list_products(
        self, filters: dict, page: int, page_size: int
    ) -> list[dict]:
        skip = (page - 1) * page_size
        products = (
            self.collection.find(filters).skip(skip).limit(page_size).to_list()
        )
        return products

    def count_products(self, filters: dict) -> int:
        return self.collection.count_documents(filters)

    @staticmethod
    def get_product_by_id_query(product_id: str) -> dict:
        query = {"_id": ObjectId(product_id)}
        return query
