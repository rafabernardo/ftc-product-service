from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.products import router
from core.dependency_injection import Container
from models.product import Product
from services.product_service import ProductService

client = TestClient(router)


@pytest.fixture
def product_service_mock():
    return Mock(spec=ProductService)


@pytest.fixture
def container(product_service_mock):
    container = Container()
    container.product_service.override(product_service_mock)
    return container


@pytest.fixture(autouse=True)
def setup(container):
    container.init_resources()
    container.wire(modules=[__name__])
    yield
    container.unwire()


def test_list_product(product_service_mock):
    # Arrange

    expected_products = [
        Product(
            id="67a77edeaf970c68f41cc3d3",
            name="Test Product",
            price=1000,
            description="Test description",
            image="test-image.jpg",
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
            category="meal",
        ),
    ]
    product_service_mock.list_products.return_value = expected_products
    product_service_mock.count_products.return_value = 1

    response = client.get(
        "/products/", params={"category": "meal", "page": 1, "page_size": 10}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    product_service_mock.list_products.assert_called_once()
