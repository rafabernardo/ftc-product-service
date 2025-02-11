from unittest.mock import MagicMock

import pytest

from core.exceptions.commons_exceptions import NoDocumentsFoundException
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


def test_identify_user_success(
    user_service: UserService,
    user_repository: UserMongoRepository,
    user_mock_without_cpf: User,
):
    user_repository.get_by_id.return_value = user_mock_without_cpf
    user_repository.update_entity.return_value = user_mock_without_cpf

    result = user_service.identify_user(user_mock_without_cpf.id, "54768430007")

    assert isinstance(result, User)
    assert result.cpf == user_mock_without_cpf.cpf


def test_identify_user_with_no_existing_id(
    user_service: UserService,
    user_repository: UserMongoRepository,
    user_mock: User,
):
    user_repository.get_by_id.return_value = None

    with pytest.raises(NoDocumentsFoundException, match="No document found"):
        user_service.identify_user(user_mock.id, "54768430007")


def test_identify_user_invalid_cpf(
    user_service: UserService,
    user_repository: UserMongoRepository,
    user_mock_without_cpf: User,
):
    user_repository.get_by_id.return_value = user_mock_without_cpf
    user_repository.update_entity.return_value = user_mock_without_cpf

    with pytest.raises(UserInvalidFormatDataError, match="Invalid CPF format"):
        user_service.identify_user(user_mock_without_cpf.id, "54768430000")


def test_identify_user_already_have_cpf(
    user_service: UserService,
    user_repository: UserMongoRepository,
    user_mock: User,
):
    user_repository.get_by_id.return_value = user_mock
    user_repository.update_entity.return_value = user_mock

    with pytest.raises(UserAlreadyExistsError, match="User already has a CPF"):
        user_service.identify_user(user_mock.id, "54768430000")
