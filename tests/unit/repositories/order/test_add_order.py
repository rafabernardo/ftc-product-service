from datetime import datetime

import pytest

from core.dependency_injection import Container
from models.order import Order, OrderItem, Status
from models.product import Product
from repositories.order_repository import OrderMongoRepository


@pytest.fixture
def mock_order() -> Order:
    return Order(
        products=[
            OrderItem(
                product=Product(
                    id="67a77edeaf970c68f41cc3d3",
                    name="Test Product",
                    category="meal",
                    price=10,
                    description="Test description",
                    image="test-image.jpg",
                ),
                quantity=1,
                price=10,
            )
        ],
        owner_id="67a77edeaf970c68f41cc3d3",
        status="pending",
        payment_status="pending",
        total_price=10,
        order_number=1,
    )


@pytest.fixture
def order_repository(container: Container, mock_mongo_db):
    repository: OrderMongoRepository = container.order_repository()
    yield repository


def test_add_order_successfully(
    mock_order, order_repository: OrderMongoRepository
):
    result = order_repository.add(mock_order)

    # Assert
    assert result is not None
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    assert result.status == Status.pending.value
