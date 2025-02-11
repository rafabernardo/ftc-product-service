from unittest.mock import MagicMock

import pytest

from core.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from models.user import User
from repositories.user_repository import UserMongoRepository
from services.user_service import UserService


@pytest.fixture
def user_repository():
    repository = MagicMock()  # Mock the entire repository
    return repository


@pytest.fixture
def user_service(user_repository):
    user_service = UserService(repository=user_repository)
    return user_service


def test_register_user_success(
    user_service: UserService, user_repository: UserMongoRepository, user_mock
):
    user = User(
        name="Rafaela",
        email="email@email.com",
        cpf="54768430007",
    )
    user_repository.exists_by_cpf.return_value = False
    user_repository.add.return_value = user_mock

    result = user_service.register_user(user)

    assert isinstance(result, User)
    assert result.cpf == "54768430007"


def test_register_user_success_without_cpf(
    user_service: UserService,
    user_repository: UserMongoRepository,
    user_mock_without_cpf,
):
    user = User(
        name="Rafaela",
        email="email@email.com",
    )
    user_repository.add.return_value = user_mock_without_cpf

    result = user_service.register_user(user)

    assert isinstance(result, User)
    assert result.email == user.email


def test_register_user_invalid_email(user_service: UserService):
    user = User(
        email="invalid_email",
        cpf="547.684.300-07",
        name="Rafaela",
    )

    with pytest.raises(
        UserInvalidFormatDataError, match="Invalid email format"
    ):
        user_service.register_user(user)


def test_register_user_invalid_cpf(user_service: UserService):
    user = User(
        email="test@example.com",
        cpf="invalid_cpf",
        name="Rafaela",
    )

    with pytest.raises(UserInvalidFormatDataError, match="Invalid CPF format"):
        user_service.register_user(user)


def test_register_user_cpf_already_exists(
    user_service,
    user_repository: UserMongoRepository,
):
    user = User(
        email="test@example.com",
        cpf="547.684.300-07",
        name="Rafaela",
    )
    user_repository.exists_by_cpf.return_value = True

    with pytest.raises(
        UserAlreadyExistsError, match="A user with this CPF already exists"
    ):
        user_service.register_user(user)
