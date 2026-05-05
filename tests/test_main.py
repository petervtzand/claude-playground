from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_status_code():
    response = client.get("/")
    assert response.status_code == 200


def test_root_body():
    response = client.get("/")
    assert response.json() == {"message": "Hello from Claude Playground!"}


def test_health_status_code():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_body():
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_version_status_code():
    response = client.get("/version")
    assert response.status_code == 200


def test_version_body():
    response = client.get("/version")
    assert response.json() == {"version": "0.1.0"}
