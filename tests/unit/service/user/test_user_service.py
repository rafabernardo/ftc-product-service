from unittest.mock import Mock, patch

import pytest

from core.exceptions.commons_exceptions import NoDocumentsFoundException
from core.exceptions.user_exceptions import UserInvalidFormatDataError
from services.user_service import UserService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def user_service(mock_repository):
    return UserService(repository=mock_repository)


def test_list_users(user_service, mock_repository, user_mock):
    mock_repository.list_entities.return_value = [user_mock, user_mock]
    users = user_service.list_users()
    assert len(users) == 2
    mock_repository.list_entities.assert_called_once()


def test_get_user_by_cpf_valid(user_service, mock_repository, user_mock):
    cpf = user_mock.cpf
    mock_repository.get_by_cpf.return_value = user_mock

    with patch("services.user_service.validate_cpf", return_value=True):
        with patch("services.user_service.clean_cpf_to_db", return_value=cpf):
            result = user_service.get_user_by_cpf(cpf)
            assert result == user_mock
            mock_repository.get_by_cpf.assert_called_once_with(cpf)


def test_get_user_by_cpf_invalid(user_service):
    cpf = "invalid_cpf"
    with patch("services.user_service.validate_cpf", return_value=False):
        with pytest.raises(UserInvalidFormatDataError):
            user_service.get_user_by_cpf(cpf)


def test_get_user_by_id(user_service, mock_repository, user_mock):
    user_id = user_mock.id
    mock_repository.get_by_id.return_value = user_mock
    result = user_service.get_user_by_id(user_id)
    assert result == user_mock
    mock_repository.get_by_id.assert_called_once_with(user_id)


def test_delete_user_existing(user_service, mock_repository, user_mock):
    user_id = user_mock.id
    mock_repository.exists_by_id.return_value = True
    mock_repository.delete_entity.return_value = True
    result = user_service.delete_user(user_id)
    assert result is True
    mock_repository.exists_by_id.assert_called_once_with(user_id)
    mock_repository.delete_entity.assert_called_once_with(user_id)


def test_delete_user_non_existing(user_service, mock_repository):
    user_id = "user_id"
    mock_repository.exists_by_id.return_value = False
    with pytest.raises(NoDocumentsFoundException):
        user_service.delete_user(user_id)
    mock_repository.exists_by_id.assert_called_once_with(user_id)
