from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
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


def test_get_product_by_id_success(product_service_mock):
    product_service_mock.get_product_by_id.return_value = Product(
        id="67a77edeaf970c68f41cc3d3",
        name="Test Product",
        price=1000,
        description="Test description",
        image="test-image.jpg",
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
        category="meal",
    )

    response = client.get("/products/67a77edeaf970c68f41cc3d3")

    assert response.status_code == 200
    assert response.json()["id"] == "67a77edeaf970c68f41cc3d3"


def test_get_product_by_id_not_found(product_service_mock):
    product_service_mock.get_product_by_id.return_value = None
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.get("/products/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 404
        assert response.json() == {"detail": "No documents found"}


def test_get_product_by_id_internal_server_error(product_service_mock):
    product_service_mock.get_product_by_id.side_effect = Exception(
        "Unexpected error"
    )
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.get("/products/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
