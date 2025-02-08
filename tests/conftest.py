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
def container():
    return Container()


@pytest.fixture
def mock_mongo_db(container: Container):
    container.mongo_database.override(providers.Factory(mocked_database))
    yield
    container.mongo_database.reset_override()


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("API_PORT", 0000)
    monkeypatch.setenv("MONGO_URL", "")
    monkeypatch.setenv("MONGO_PORT", 000)
    monkeypatch.setenv("MONGO_USERNAME", "")
    monkeypatch.setenv("MONGO_PASSWORD", "")
    monkeypatch.setenv("MONGO_DATABASE", "")

    yield
