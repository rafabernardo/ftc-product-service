from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.orders import router
from core.dependency_injection import Container
from services.order_service import OrderService

client = TestClient(router)


@pytest.fixture
def order_service_mock():
    return Mock(spec=OrderService)


@pytest.fixture
def container(order_service_mock):
    container = Container()
    container.order_service.override(order_service_mock)
    return container


@pytest.fixture(autouse=True)
def setup(container):
    container.init_resources()
    container.wire(modules=[__name__])
    yield
    container.unwire()


def test_delete_order_sucess(
    order_service_mock,
):
    order_service_mock.delete_order.return_value = True

    response = client.delete("/orders/67a77edeaf970c68f41cc3d4")

    assert response.status_code == 204
