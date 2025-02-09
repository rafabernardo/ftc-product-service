from datetime import datetime

import pytest

from src.core.dependency_injection import Container
from src.models.product import Product
from src.repositories.product_repository import ProductMongoRepository


@pytest.fixture
def mock_product() -> Product:
    return Product(
        name="Test Product",
        category="meal",
        price=1000,
        description="Test description",
        image="test-image.jpg",
    )


@pytest.fixture
def product_repository(container: Container, mock_mongo_db):
    repository: ProductMongoRepository = container.product_repository()
    yield repository


def test_add_product_successfully(
    mock_product, product_repository: ProductMongoRepository
):
    result = product_repository.add(mock_product)

    # Assert
    assert result is not None
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
