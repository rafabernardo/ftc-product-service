from core.settings import get_settings
from external.parser import prepare_order_to_payment
from external.payment import register_payment
from models.order import Order
from services.order_number_service import OrderNumberService

order_number_service = OrderNumberService()
settings = get_settings()


class PaymentService:
    async def register_payment(self, order: Order) -> Order:
        payment_data = prepare_order_to_payment(order)
        await register_payment(token="", payload=payment_data)
