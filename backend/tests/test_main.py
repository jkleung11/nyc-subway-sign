import pytest
from unittest.mock import MagicMock, patch
from asgi_lifespan import LifespanManager

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.service.subway_system.ROUTE_ENDPOINT_DICT", {
    "A": "test-url-ACE",
    "B": "test-url-BDFM"
})
async def test_routes():
    # Use LifespanManager to manage the app's lifespan
    async with LifespanManager(app):
        with TestClient(app) as client:
            response = client.get("/routes")
            assert response.status_code == 200
            assert [*response.json()['routes'].keys()] == ["A", "B"]

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "hello world"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "app is healthy"