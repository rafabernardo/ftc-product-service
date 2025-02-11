from unittest.mock import Mock

import mongomock
import pytest
from dependency_injector import providers

from models.user import User
from src.core.dependency_injection import Container


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
def user_mock():
    return User(
        id="67a77edeaf970c68f41cc3d3",
        name="Rafaela",
        email="email@email.com",
        cpf="54768430007",
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )


@pytest.fixture
def user_mock_without_cpf():
    return User(
        id="67a77edeaf970c68f41cc3d3",
        name="Rafaela",
        email="email@email.com",
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )
