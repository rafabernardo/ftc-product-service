from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
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


def test_get_user_by_id_success(user_service_mock):
    user_service_mock.get_user_by_id.return_value = {
        "id": "67a77edeaf970c68f41cc3d3",
        "name": "Rafaela",
        "email": "email@email.com",
        "cpf": "44713529036",
        "created_at": "2025-02-08T12:57:18.267Z",
        "updated_at": "2025-02-08T12:57:18.267Z",
    }

    response = client.get("/users/67a77edeaf970c68f41cc3d3")

    assert response.status_code == 200
    assert response.json()["id"] == "67a77edeaf970c68f41cc3d3"


def test_get_user_by_id_not_found(user_service_mock):
    user_service_mock.get_user_by_id.return_value = None
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.get("/users/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 404
        assert response.json() == {"detail": "No documents found"}


def test_get_user_by_id_internal_server_error(user_service_mock):
    user_service_mock.get_user_by_id.side_effect = Exception("Unexpected error")
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.get("/users/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
