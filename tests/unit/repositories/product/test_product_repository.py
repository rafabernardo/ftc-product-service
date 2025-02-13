from bson import ObjectId

from repositories.product_repository import ProductMongoRepository


def test_get_product_by_id_query():
    product_id = "507f1f77bcf86cd799439011"
    expected_query = {"_id": ObjectId(product_id)}
    assert (
        ProductMongoRepository.get_product_by_id_query(product_id)
        == expected_query
    )


def test_get_list_product_query():
    expected_query = {}
    assert ProductMongoRepository.get_list_product_query() == expected_query


def test_get_product_update_data():
    kwargs = {"name": "New Product", "price": 100}
    expected_update_data = {"$set": kwargs}
    assert (
        ProductMongoRepository.get_product_update_data(kwargs)
        == expected_update_data
    )
