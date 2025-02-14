from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.v1.exceptions.commons import (
    InternalServerErrorHTTPException,
    NoDocumentsFoundHTTPException,
)
from api.v1.products import router
from core.dependency_injection import Container
from core.exceptions.commons_exceptions import NoDocumentsFoundException
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


def test_delete_product_success(product_service_mock):
    product_service_mock.delete_product.return_value = True
    response = client.delete("/products/67a77edeaf970c68f41cc3d3")

    assert response.status_code == 204


def test_delete_product_not_found(product_service_mock):
    product_service_mock.delete_product.side_effect = (
        NoDocumentsFoundException()
    )
    with pytest.raises(
        NoDocumentsFoundHTTPException, match="No document found"
    ):

        response = client.delete("/products/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 404
        assert response.json() == {"detail": "No documents found"}


def test_delete_order_internal_server_error(product_service_mock):
    product_service_mock.delete_product.side_effect = Exception(
        "Unexpected error"
    )
    with pytest.raises(
        InternalServerErrorHTTPException, match="Internal server error"
    ):
        response = client.delete("/products/67a77edeaf970c68f41cc3d3")

        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
