from datetime import datetime

import pytest

from core.dependency_injection import Container
from models.user import User
from repositories.user_repository import UserMongoRepository


@pytest.fixture
def mock_user() -> User:
    return User(name="Rafaela", email="rafaela@email.com", cpf="44713529036")


@pytest.fixture
def user_repository(container: Container, mock_mongo_db):
    repository: UserMongoRepository = container.user_repository()
    yield repository


def test_add_user_successfully(mock_user, user_repository: UserMongoRepository):
    result = user_repository.add(mock_user)

    # Assert
    assert result is not None
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    assert isinstance(result, User)
