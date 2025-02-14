from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

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


def test_get_user_by_id_success(user_service_mock, user_mock):
    user_id = "67a77edeaf970c68f41cc3d3"
    request_data = {"cpf": "54768430007"}

    user_service_mock.identify_user.return_value = user_mock

    response = client.patch(f"users/identify/{user_id}", json=request_data)

    assert response.status_code == 200
