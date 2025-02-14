from unittest.mock import create_autospec

import pytest

from core.exceptions.commons_exceptions import NoDocumentsFoundException
from db.mongodb.interfaces.product import ProductsRepositoryInterface
from models.product import Product
from services.product_service import ProductService


def test_update_product_success():
    # Arrange
    repository = create_autospec(ProductsRepositoryInterface)
    product_service = ProductService(repository)
    product_id = "67a77edeaf970c68f41cc3d3"
    update_data = {"name": "Updated Product"}
    updated_product = (
        Product(
            id="67a77edeaf970c68f41cc3d3",
            name="TUpdated Product",
            price=1000,
            description="Test description",
            image="test-image.jpg",
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
            category="meal",
        ),
    )

    repository.exists_by_id.return_value = True
    repository.update_entity.return_value = updated_product

    # Act
    result = product_service.update_product(product_id, **update_data)

    # Assert
    repository.exists_by_id.assert_called_once_with(product_id)
    repository.update_entity.assert_called_once_with(product_id, **update_data)
    assert result == updated_product


def test_update_product_not_found():
    # Arrange
    repository = create_autospec(ProductsRepositoryInterface)
    product_service = ProductService(repository)
    product_id = "123"
    update_data = {"name": "Updated Product"}

    repository.exists_by_id.return_value = False

    # Act & Assert
    with pytest.raises(NoDocumentsFoundException):
        product_service.update_product(product_id, **update_data)

    repository.exists_by_id.assert_called_once_with(product_id)
    repository.update_entity.assert_not_called()
