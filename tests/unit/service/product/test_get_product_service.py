from unittest.mock import MagicMock

import pytest

from models.product import Product
from repositories.product_repository import ProductMongoRepository
from services.product_service import ProductService


@pytest.fixture
def product_repository():
    repository = MagicMock()  # Mock the entire repository
    return repository


@pytest.fixture
def product_service(product_repository):
    product_service = ProductService(repository=product_repository)
    return product_service


def test_register_product_success(
    product_service: ProductService,
    product_repository: ProductMongoRepository,
    mock_product: Product,
):
    product_repository.get_by_id.return_value = Product(
        id="67a77edeaf970c68f41cc3d3",
        name="Test Product",
        price=1000,
        description="Test description",
        image="test-image.jpg",
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
        category="meal",
    )

    result = product_service.get_product_by_id("67a77edeaf970c68f41cc3d3")

    assert isinstance(result, Product)
    assert result.created_at is not None
    assert result.updated_at is not None
