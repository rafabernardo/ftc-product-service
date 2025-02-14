import abc

from db.mongodb.interfaces.base import BaseRepositoryInterface
from models.order import Order, OrderFilter, OrderItem


class OrderRepositoryInterface(BaseRepositoryInterface[Order]):
    @abc.abstractmethod
    def add(self, order: Order) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_entities(
        self, filter_params: OrderFilter, page: int, page_size: int, sort: dict
    ) -> list[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_order_item(self, order_id: str, order_item: OrderItem) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_order_items_by_order_id(self, order_id) -> list[OrderItem]:
        raise NotImplementedError
