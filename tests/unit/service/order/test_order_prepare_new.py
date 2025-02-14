from unittest.mock import MagicMock

import pytest
from bson import ObjectId

from services.order_service import OrderService


@pytest.fixture
def order_repository():
    return MagicMock()


@pytest.fixture
def order_service(order_repository):
    return OrderService(order_repository)


def test_prepare_new_order_with_valid_data(order_service):
    mock_product = {
        "_id": ObjectId(),
        "name": "Test Product",
        "price": 100,  # Price in cents
        "description": "Testing description",
        "image": "image.jpg",
        "category": "meal",
    }

    order_data = {
        "id": str(ObjectId()),
        "status": "pending",
        "order_number": 12345,
        "owner_id": str(ObjectId()),
        "payment_status": "pending",
        "paid_at": None,
    }
    products_data = [
        {"product": mock_product, "price": 100, "quantity": 1},
        {"product": mock_product, "price": 100, "quantity": 1},
    ]

    new_order = order_service.prepare_new_order(order_data, products_data)

    assert new_order.id == order_data["id"]
    assert new_order.total_price == 200
    assert new_order.status == "pending"
    assert new_order.payment_status == "pending"
    assert len(new_order.products) == 2
