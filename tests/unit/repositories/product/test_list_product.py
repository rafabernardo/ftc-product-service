from unittest.mock import MagicMock

from models.product import Product
from repositories.product_repository import ProductMongoRepository


def test_get_products_with_pagination(mock_mongo_collection):
    # Mock data
    mock_products = [
        {
            "_id": "67a77edeaf970c68f41cc3d3",
            "name": "Test Product",
            "price": 100.0,
            "description": "Test description",
            "image": "test-image.jpg",
            "created_at": "2025-02-08T12:57:18.267Z",
            "updated_at": "2025-02-08T12:57:18.267Z",
            "category": "meal",
        },
        {
            "_id": "67a77edeaf970c68f41cc3d4",
            "name": "Test Product 2",
            "price": 100.0,
            "description": "Test description 2",
            "image": "test-image2.jpg",
            "created_at": "2025-02-08T12:57:18.267Z",
            "updated_at": "2025-02-08T12:57:18.267Z",
            "category": "beverage",
        },
    ]

    # Create the chain of mocks
    mock_find = MagicMock()
    mock_skip = MagicMock()
    mock_limit = MagicMock()

    mock_limit.return_value = mock_products
    mock_skip.return_value = mock_limit
    mock_find.return_value = mock_skip

    mock_mongo_collection.find.return_value = mock_find
    mock_mongo_collection.find.return_value.skip.return_value = mock_skip
    mock_mongo_collection.find.return_value.skip.return_value.limit.return_value = (  # noqa: E501
        mock_limit
    )
    mock_mongo_collection.find.return_value.skip.return_value.limit.return_value = (  # noqa: E501
        mock_products
    )

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_mongo_collection  # Simulate db["collection_name"]
    )

    repo = ProductMongoRepository(database=mock_db)

    result = repo.list_entities(filter_params={}, page=1, page_size=5)

    assert result is not None
    assert len(result) == 2
    mock_mongo_collection.find.assert_called_once()
    mock_mongo_collection.find.return_value.skip.assert_called_once_with(0)
    mock_mongo_collection.find.return_value.skip.return_value.limit.assert_called_once_with(
        5
    )
    assert isinstance(result[0], Product)
