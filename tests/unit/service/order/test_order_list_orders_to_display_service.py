from unittest.mock import MagicMock

import pytest

from models.order import Order, OrderItem, OrderOutput, Status
from models.product import Product
from repositories.order_repository import OrderMongoRepository
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


@pytest.fixture
def order():
    return Order(
        id="67a77edeaf970c68f41cc3d4",
        order_number="12345",
        status=Status.ready.value,
        paid_at="2025-02-08T12:57:18.267",
        payment_status="paid",
        total_price=10,
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
        owner_id="67a77edeaf970c68f41cc3d5",
    )


@pytest.fixture
def order_second():
    return Order(
        id="67a77edeaf970c68f41cc3d4",
        order_number="12345",
        status=Status.being_prepared.value,
        paid_at="2025-02-08T12:57:18.267",
        payment_status="paid",
        total_price=10,
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
        owner_id="67a77edeaf970c68f41cc3d5",
    )


def test_list_order_to_display(
    order_service: OrderService,
    order_repository: OrderMongoRepository,
    order: Order,
    order_second: Order,
):
    order_repository.list_entities.return_value = [order, order_second]
    result = order_service.list_orders_to_display(page=1, page_size=5)

    assert isinstance(result, list)
    assert isinstance(result[0], OrderOutput)
    assert isinstance(result[1], OrderOutput)
