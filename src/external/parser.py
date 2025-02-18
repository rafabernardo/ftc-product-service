from core.settings import get_settings
from models.order import Order

settings = get_settings()


def prepare_order_to_payment(order: Order) -> dict:
    callback_url = f"http://{settings.API_URL}/v1/payments/{order.id}"
    print(f"callback_url | {callback_url}")

    return {
        "event": f"my_event_{order.id}",
        "customer_id": "1234",
        "amount": str(order.total_price),
        "currency": "BRL",
        "metadata": {
            "order_reference": order.id,
            "user_reference": order.owner_id,
        },
        "callback_url": callback_url,
    }
