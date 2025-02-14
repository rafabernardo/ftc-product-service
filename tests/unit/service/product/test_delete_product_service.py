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
    product_repository.delete_entity.return_value = True
    product_repository.exists_by_id.return_value = True

    result = product_service.delete_product("67a77edeaf970c68f41cc3d3")

    assert isinstance(result, bool)
    assert result is True
