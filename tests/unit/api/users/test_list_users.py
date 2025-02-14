from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import InternalServerErrorHTTPException
from api.v1.models.user import UserV1Response
from api.v1.users import router
from core.dependency_injection import Container
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


def test_list_users(user_service_mock):
    user_service_mock.list_users.return_value = [
        UserV1Response(
            id="67a77edeaf970c68f41cc3d3",
            name="Rafaela",
            email="email@email.com",
            cpf="54768430007",
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
        )
    ]

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 1
    user_service_mock.list_users.assert_called_once()


def test_list_users_internal_server_error(user_service_mock):
    user_service_mock.list_users.side_effect = Exception(
        "Internal server error"
    )
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.get("/users")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
