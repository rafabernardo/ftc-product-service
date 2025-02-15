from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.orders import router
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
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


async def validate_token(
    token: str,
):
    """Mock JWT verification, returning a fake decoded payload."""
    return {"valid": True}


@patch("api.v1.orders.validate_token", validate_token)
def test_delete_order_sucess(
    order_service_mock,
):
    order_service_mock.delete_order.return_value = True

    response = client.delete(
        "/orders/67a77edeaf970c68f41cc3d4",
        headers={"Authorization": "Bearer asda"},
    )

    assert response.status_code == 204


@patch("api.v1.orders.validate_token", validate_token)
def test_delete_order_not_found(order_service_mock):
    order_service_mock.delete_order.side_effect = NoDocumentsFoundException()
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.delete(
            "/orders/67a77edeaf970c68f41cc3d3",
            headers={"Authorization": "Bearer asda"},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "No documents found"}


@patch("api.v1.orders.validate_token", validate_token)
def test_delete_order_internal_server_error(order_service_mock):
    order_service_mock.delete_order.side_effect = Exception("Unexpected error")
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.delete(
            "/orders/67a77edeaf970c68f41cc3d3",
            headers={"Authorization": "Bearer asda"},
        )

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
