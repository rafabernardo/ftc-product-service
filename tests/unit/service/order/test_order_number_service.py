import threading

from services.order_number_service import OrderNumberService


def test_singleton_instance():
    instance1 = OrderNumberService()
    instance2 = OrderNumberService()
    assert instance1 is instance2, "OrderNumberService is not a singleton"


def test_initial_order_number():
    service = OrderNumberService()
    assert (
        service.get_next_order_number() == 1
    ), "Initial order number should be 1"


def test_sequential_order_numbers():
    service = OrderNumberService()
    first_order_number = service.get_next_order_number()
    second_order_number = service.get_next_order_number()
    assert (
        second_order_number == first_order_number + 1
    ), "Order numbers are not sequential"


def test_thread_safety():
    service = OrderNumberService()
    order_numbers = set()

    def get_order_number():
        order_numbers.add(service.get_next_order_number())

    threads = [threading.Thread(target=get_order_number) for _ in range(100)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert (
        len(order_numbers) == 100
    ), "Order numbers are not unique across threads"
