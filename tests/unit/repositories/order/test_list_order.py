from datetime import datetime
from unittest.mock import MagicMock

from bson import ObjectId

from models.order import Order, OrderFilter
from repositories.order_repository import OrderMongoRepository


def test_get_order_with_pagination(mock_mongo_collection):
    mock_product = {
        "_id": ObjectId(),
        "name": "Test Product",
        "price": 10,  # Price in cents
        "description": "Testing description",
        "image": "image.jpg",
        "category": "meal",
    }

    mock_orders = [
        {
            "_id": ObjectId(),
            "status": "pending",
            "products": [
                {
                    "product": mock_product,
                    "quantity": 1,
                    "price": 10,  # Price in cents
                }
            ],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "order_number": 12345,
            "owner_id": str(ObjectId()),
            "payment_status": "pending",
            "paid_at": None,
            "total_price": 10,  # Total price in cents
        },
        {
            "_id": ObjectId(),
            "status": "pending",
            "products": [
                {
                    "product": mock_product,
                    "quantity": 2,
                    "price": 20,  # Price in cents
                }
            ],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "order_number": 12345,
            "owner_id": str(ObjectId()),
            "payment_status": "pending",
            "paid_at": None,
            "total_price": 20,  # Total price in cents
        },
    ]

    # Create the chain of mocks
    mock_find = MagicMock()
    mock_skip = MagicMock()
    mock_limit = MagicMock()

    mock_limit.return_value = mock_orders
    mock_skip.return_value = mock_limit
    mock_find.return_value = mock_skip

    mock_mongo_collection.find.return_value = mock_find
    mock_mongo_collection.find.return_value.skip.return_value = mock_skip
    mock_mongo_collection.find.return_value.skip.return_value.limit.return_value = (  # noqa: E501
        mock_limit
    )
    mock_mongo_collection.find.return_value.skip.return_value.limit.return_value = (  # noqa: E501
        mock_orders
    )

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_mongo_collection  # Simulate db["collection_name"]
    )

    repo = OrderMongoRepository(database=mock_db)
    order_filter = OrderFilter(status=None)

    result = repo.list_entities(
        filter_params=order_filter, page=1, page_size=5, sort=None
    )

    assert result is not None
    assert len(result) == 2
    mock_mongo_collection.find.assert_called_once()
    mock_mongo_collection.find.return_value.skip.assert_called_once_with(0)
    mock_mongo_collection.find.return_value.skip.return_value.limit.assert_called_once_with(
        5
    )
    assert isinstance(result[0], Order)
