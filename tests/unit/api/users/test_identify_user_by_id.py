from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
    UnprocessableEntityErrorHTTPException,
)
from api.v1.users import router
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
from core.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from services.user_service import UserService

client = TestClient(router)


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def container(user_service_mock):
    container = Container()
    container.user_service.override(user_service_mock)
    return container


@pytest.fixture(autouse=True)
def setup(container):
    container.init_resources()
    container.wire(modules=[__name__])
    yield
    container.unwire()


def test_get_user_by_id_success(user_service_mock, user_mock):
    user_id = "67a77edeaf970c68f41cc3d3"
    request_data = {"cpf": "54768430007"}

    user_service_mock.identify_user.return_value = user_mock

    response = client.patch(f"users/identify/{user_id}", json=request_data)

    assert response.status_code == 200


def test_identify_user_no_documents_found(user_service_mock):
    user_id = "123"
    request_data = {"cpf": "12345678900"}

    user_service_mock.identify_user.side_effect = NoDocumentsFoundException()
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.patch(f"users/identify/{user_id}", json=request_data)

        assert response.status_code == 404


def test_identify_user_invalid_format(user_service_mock):
    user_id = "123"
    request_data = {"cpf": "invalid_cpf"}

    user_service_mock.identify_user.side_effect = UserInvalidFormatDataError(
        "Invalid CPF format"
    )
    with pytest.raises(
        UnprocessableEntityErrorHTTPException, match="Invalid CPF format"
    ):

        response = client.patch(f"users/identify/{user_id}", json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid CPF format"


def test_identify_user_already_exists(user_service_mock):
    user_id = "123"
    request_data = {"cpf": "12345678900"}

    user_service_mock.identify_user.side_effect = UserAlreadyExistsError(
        "User already has a CPF"
    )

    with pytest.raises(
        UnprocessableEntityErrorHTTPException, match="User already has a CPF"
    ):
        response = client.patch(f"users/identify/{user_id}", json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"] == "User already has a CPF"


def test_identify_user_internal_server_error(user_service_mock):
    user_id = "123"
    request_data = {"cpf": "12345678900"}

    user_service_mock.identify_user.side_effect = Exception(
        "Internal server error"
    )

    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.patch(f"users/identify/{user_id}", json=request_data)

        assert response.status_code == 500
