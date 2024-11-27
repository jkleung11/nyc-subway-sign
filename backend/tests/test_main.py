import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "hello world"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "app is healthy"