from unittest.mock import Mock

import mongomock
import pytest
from dependency_injector import providers

from src.core.dependency_injection import Container


@pytest.fixture
def mock_mongo_collection():
    collection_mock = Mock()
    return collection_mock


def mocked_database():
    client_mock = mongomock.MongoClient()
    return client_mock.db


@pytest.fixture
def container(mock_env):
    return Container()


@pytest.fixture
def mock_mongo_db(container: Container):
    container.mongo_database.override(providers.Factory(mocked_database))
    yield
    container.mongo_database.reset_override()
