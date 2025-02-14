from unittest.mock import MagicMock

import pytest

from models.product import Product
from services.order_service import OrderService
from services.product_service import ProductService


@pytest.fixture
def order_repository():
    repository = MagicMock()  # Mock the entire repository
    return repository


@pytest.fixture
def product_repository():
    repository = MagicMock()  # Mock the entire repository
    return repository


@pytest.fixture
def order_service(order_repository):
    order_service = OrderService(repository=order_repository)
    return order_service


@pytest.fixture
def product_service(product_repository):
    product_service = ProductService(repository=product_repository)
    return product_service


def test_register_order_success(
    order_service: OrderService,
    product_service: ProductService,
    product_repository,
):
    order_items = [{"product_id": "67a77edeaf970c68f41cc3d3", "quantity": 1}]

    product_repository.get_by_id.side_effect = lambda product_id: Product(
        id="67a77edeaf970c68f41cc3d3",
        name="Test Product",
        category="meal",
        price=10,
        description="Test description",
        image="test-image.jpg",
    )
    result = order_service.get_order_items_details(order_items, product_service)

    assert isinstance(result, list)
    assert len(result) == 1
