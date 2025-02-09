from datetime import datetime
from unittest.mock import MagicMock

from bson import ObjectId

from models.order import Order, Status
from repositories.order_repository import OrderMongoRepository


def test_get_order_by_id_found(mock_mongo_collection):
    # Mock data for Product
    mock_product = {
        "_id": ObjectId(),
        "name": "Test Product",
        "price": 1000,  # Price in cents
        "description": "Testing description",
        "image": "image.jpg",
        "category": "meal",
    }

    # Mock data for OrderItem
    mock_order_item = {
        "product": mock_product,
        "quantity": 2,
        "price": 2000,  # Price in cents
    }

    # Mock data for Order
    mock_order = {
        "_id": ObjectId(),
        "status": "pending",
        "products": [mock_order_item],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "order_number": 12345,
        "owner_id": str(ObjectId()),
        "payment_status": "pending",
        "paid_at": None,
        "total_price": 2000,  # Total price in cents
    }

    mock_collection = MagicMock()
    mock_collection.find_one.return_value = mock_order

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = OrderMongoRepository(database=mock_db)

    result = repo.get_by_id(mock_order["_id"])

    assert result is not None
    assert isinstance(result, Order)
    assert result.id == str(mock_order["_id"])
    assert result.status == Status.pending.value
    assert result.owner_id == str(mock_order["owner_id"])
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
