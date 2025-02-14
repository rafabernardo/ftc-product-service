from unittest.mock import MagicMock

import pytest

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
):
    product_repository.count_entities.return_value = 1

    result = product_service.count_products(filter_prod={})

    assert isinstance(result, int)
    assert result == 1
