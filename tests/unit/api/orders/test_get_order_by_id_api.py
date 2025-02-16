from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from api.v1.orders import router
from core.dependency_injection import Container
from models.order import OrderItem, OrderOutput, Status
from models.product import Product
from services.order_service import OrderService
from services.user_service import UserService

client = TestClient(router)


@pytest.fixture
def order_service_mock():
    return Mock(spec=OrderService)


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def container(order_service_mock, user_service_mock):
    container = Container()
    container.order_service.override(order_service_mock)
    container.user_service.override(user_service_mock)
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
def test_get_order_by_id(order_service_mock, user_service_mock, user_mock):
    user_service_mock.get_user_by_id.return_value = user_mock

    order_service_mock.get_order_by_id.return_value = OrderOutput(
        id="67a77edeaf970c68f41cc3d4",
        order_number="12345",
        status=Status.being_prepared.value,
        paid_at="2025-02-08T12:57:18.267+00:00",
        payment_status="paid",
        total_price=10,
        products=[
            OrderItem(
                product=Product(
                    id="67a77edeaf970c68f41cc3d3",
                    name="Test Product",
                    category="meal",
                    price=10,
                    description="Test description",
                    image="test-image.jpg",
                    created_at="2025-02-08T12:57:18.267Z",
                    updated_at="2025-02-08T12:57:18.267Z",
                ),
                quantity=1,
                price=10,
            )
        ],
        owner_id="67a77edeaf970c68f41cc3d3",
        waiting_time=3000,
    )

    response = client.get(
        "/orders/67a77edeaf970c68f41cc3d4",
        headers={"Authorization": "Bearer asda"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == "67a77edeaf970c68f41cc3d4"
