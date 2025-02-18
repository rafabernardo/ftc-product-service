from unittest.mock import Mock

import pytest

from core.exceptions.commons_exceptions import NoDocumentsFoundException
from models.order import Order, OrderFilter, OrderItem
from models.product import Product
from services.order_service import OrderService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def order_service(mock_repository):
    return OrderService(repository=mock_repository)


def test_count_orders(order_service, mock_repository):
    mock_repository.count_entities.return_value = 5
    order_filter = OrderFilter()

    result = order_service.count_orders(order_filter=order_filter)

    assert result == 5
    mock_repository.count_entities.assert_called_once_with(
        filter_params=order_filter
    )


def test_delete_order_success(order_service, mock_repository, mock_order):
    mock_repository.get_by_id.return_value = Order(
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
    mock_repository.delete_entity.return_value = True

    result = order_service.delete_order("67a77edeaf970c68f41cc3d4")

    assert result is True
    mock_repository.get_by_id.assert_called_once_with(
        "67a77edeaf970c68f41cc3d4"
    )
    mock_repository.delete_entity.assert_called_once_with(
        entity_id="67a77edeaf970c68f41cc3d4"
    )


def test_delete_order_not_found(order_service, mock_repository):
    mock_repository.get_by_id.return_value = None

    with pytest.raises(NoDocumentsFoundException):
        order_service.delete_order("order_id")

    mock_repository.get_by_id.assert_called_once_with("order_id")
    mock_repository.delete_entity.assert_not_called()
