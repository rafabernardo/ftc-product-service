import pytest

from models.order import Order, OrderItem, OrderOutput, Status
from models.product import Product
from services.order_service import prepare_order_to_list


@pytest.fixture
def order():
    return Order(
        id="67a77edeaf970c68f41cc3d4",
        order_number="12345",
        status=Status.confirmed.value,
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
                ),
                quantity=1,
                price=10,
            )
        ],
        owner_id="67a77edeaf970c68f41cc3d5",
    )


def test_prepare_order_to_list(order):
    order_output = prepare_order_to_list(order)

    assert isinstance(order_output, OrderOutput)
    assert order_output.id == order.id
    assert order_output.order_number == order.order_number
    assert order_output.status == order.status
    assert order_output.payment_status == order.payment_status
    assert order_output.total_price == order.total_price
    assert order_output.products == order.products
    assert order_output.waiting_time is not None
