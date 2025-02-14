from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.users import router
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
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


def test_delete_product_success(user_service_mock):
    user_service_mock.delete_user.return_value = True
    response = client.delete("/users/delete/67a77edeaf970c68f41cc3d3")

    assert response.status_code == 204


def test_delete_product_not_found(user_service_mock):
    user_service_mock.delete_user.side_effect = NoDocumentsFoundException()
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.delete("/users/delete/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 404
        assert response.json() == {"detail": "No documents found"}


def test_delete_order_internal_server_error(user_service_mock):
    user_service_mock.delete_user.side_effect = Exception("Unexpected error")
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.delete("/users/delete/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
