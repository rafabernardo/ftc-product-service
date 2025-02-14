from datetime import datetime

import pytest

from core.dependency_injection import Container
from models.order import Status
from repositories.order_repository import OrderMongoRepository


@pytest.fixture
def order_repository(container: Container, mock_mongo_db):
    repository: OrderMongoRepository = container.order_repository()
    yield repository


def test_add_order_successfully(
    mock_order, order_repository: OrderMongoRepository
):
    result = order_repository.add(mock_order)

    # Assert
    assert result is not None
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    assert result.status == Status.pending.value
