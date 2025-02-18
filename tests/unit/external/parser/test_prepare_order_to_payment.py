import pytest

from core.settings import get_settings
from external.parser import prepare_order_to_payment
from models.order import Order, OrderItem
from models.product import Product

settings = get_settings()


@pytest.fixture
def mock_env():
    aux_env = settings.API_URL
    settings.API_URL = "my_api_url.com"
    yield
    settings.API_URL = aux_env


@pytest.fixture
def mock_order() -> Order:
    return Order(
        id="67a77edeaf970c68f41cc3d4",
        products=[
            OrderItem(
                product=Product(
                    id="67a77edeaf970c68f41cc3d3",
                    name="Test Product",
                    category="meal",
                    price=10,
                    description="Test description",
                    image="test-image.jpg",
                ),
                quantity=1,
                price=10,
            )
        ],
        owner_id="67a77edeaf970c68f41cc3d3",
        status="pending",
        payment_status="pending",
        total_price=10,
        order_number=1,
    )


@pytest.fixture
def expected_result() -> dict:
    return {
        "event": "my_event_67a77edeaf970c68f41cc3d4",
        "customer_id": "1234",
        "amount": "10",
        "currency": "BRL",
        "metadata": {
            "order_reference": "67a77edeaf970c68f41cc3d4",
            "user_reference": "67a77edeaf970c68f41cc3d3",
        },
        "callback_url": "http://my_api_url.com/v1/payments/67a77edeaf970c68f41cc3d4",
    }


def test_prepare_order_to_payment(
    mock_order: Order, expected_result: dict, mock_env
):
    result = prepare_order_to_payment(mock_order)

    assert result == expected_result
