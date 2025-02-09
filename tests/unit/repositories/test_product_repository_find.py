from unittest.mock import MagicMock

from models.product import Product
from repositories.product_repository import ProductMongoRepository


def test_get_by_id_found(mock_mongo_collection):
    product_id = "67a77edeaf970c68f41cc3d3"
    mock_product_data = {
        "_id": "67a77edeaf970c68f41cc3d3",
        "name": "Test Product",
        "price": 100.0,
        "description": "Test description",
        "image": "test-image.jpg",
        "created_at": "2025-02-08T12:57:18.267Z",
        "updated_at": "2025-02-08T12:57:18.267Z",
        "category": "meal",
    }

    mock_collection = MagicMock()
    mock_collection.find_one.return_value = mock_product_data

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = ProductMongoRepository(database=mock_db)

    result = repo.get_by_id(product_id)

    assert result is not None
    assert isinstance(result, Product)
    assert result.id == mock_product_data["_id"]
    assert result.name == mock_product_data["name"]
    assert result.price == mock_product_data["price"]
