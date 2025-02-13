from unittest.mock import Mock

import pytest

from models.product import Product
from src.services.product_service import ProductService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def product_service(mock_repository):
    return ProductService(repository=mock_repository)


def test_list_products(product_service, mock_repository, mock_product):
    # Arrange
    filter_prod = {"category": "meal"}
    page = 1
    page_size = 10
    expected_products = [
        Product(
            id="67a77edeaf970c68f41cc3d3",
            name="Test Product",
            price=1000,
            description="Test description",
            image="test-image.jpg",
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
            category="meal",
        ),
    ]
    mock_repository.list_entities.return_value = expected_products

    # Act
    result = product_service.list_products(filter_prod, page, page_size)

    # Assert
    assert result == expected_products
    mock_repository.list_entities.assert_called_once_with(
        filter_params=filter_prod, page=page, page_size=page_size
    )
