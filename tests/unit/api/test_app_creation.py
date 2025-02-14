import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_create_app(client):
    response = client.get("/health")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "Healthy"


def test_api_routes(client):
    response = client.get("/api/docs")
    assert response.status_code == 200
