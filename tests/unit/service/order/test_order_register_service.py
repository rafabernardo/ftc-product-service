from unittest.mock import MagicMock

import pytest

from models.order import Order, OrderItem
from models.product import Product
from repositories.order_repository import OrderMongoRepository
from services.order_number_service import OrderNumberService
from services.order_service import OrderService


@pytest.fixture
def order_repository():
    repository = MagicMock()  # Mock the entire repository
    return repository


@pytest.fixture
def order_number_service():
    order_number_service = MagicMock()  # Mock the entire repository
    return order_number_service


@pytest.fixture
def order_service(order_repository):
    order_service = OrderService(repository=order_repository)
    return order_service


def test_register_order_success(
    order_service: OrderService,
    order_repository: OrderMongoRepository,
    mock_order: Order,
    order_number_service: OrderNumberService,
):
    order_number_service.get_next_order_number.return_value = 1
    order_repository.add.return_value = Order(
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
        id="67a77edeaf970c68f41cc3d4",
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )

    result = order_service.register_order(mock_order)

    assert isinstance(result, Order)
    assert result.created_at is not None
    assert result.updated_at is not None
