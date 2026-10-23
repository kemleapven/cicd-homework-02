import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"CI/CD Web Application" in response.data
    assert b"Ven KemLeap" in response.data

def test_health_endpoint(client):
    """Test health check returns HTTP 200 and status UP."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert data["service"] == "cicd-web-app"
    assert "hostname" in data
    assert "timestamp" in data

def test_api_info_endpoint(client):
    """Test api info endpoint returns correct student details."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["student"] == "Ven KemLeap"
    assert "version" in data
