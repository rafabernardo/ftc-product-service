from unittest.mock import MagicMock

import pytest

from models.order import Order
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


def test_get_by_id(
    order_service: OrderService,
    order_repository: OrderMongoRepository,
    mock_order: Order,
):
    order_repository.get_by_id.return_value = mock_order
    result = order_service.get_order_by_id(
        mock_order.id,
    )

    assert isinstance(result, Order)
    assert result.id == mock_order.id
    assert result.order_number == mock_order.order_number
    assert result.status == mock_order.status
    assert result.payment_status == mock_order.payment_status
