from datetime import datetime
from unittest.mock import Mock

import mongomock
import pytest
from dependency_injector import providers

from src.core.dependency_injection import Container
from src.models.product import Product
from src.repositories.product_repository import ProductMongoRepository


@pytest.fixture
def mock_product():
    return Product(
        name="Test Product",
        category="meal",
        price=1000,
        description="Test description",
        image="test-image.jpg",
    )


@pytest.fixture
def mock_mongo_collection():
    collection_mock = Mock()
    return collection_mock


def mocked_database():
    client_mock = mongomock.MongoClient()
    return client_mock.db


@pytest.fixture
def container():
    return Container()


@pytest.fixture
def mock_mongo_db(container: Container):
    container.mongo_database.override(providers.Factory(mocked_database))
    yield
    container.mongo_database.reset_override()


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
