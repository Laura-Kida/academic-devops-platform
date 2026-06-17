from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_courses_without_token():
    response = client.get("/courses")
    assert response.status_code == 401


def test_courses_with_valid_token():
    response = client.get(
        "/courses",
        headers={
            "Authorization": "Bearer token-jwt-simulado-12345"
        }
    )

    assert response.status_code == 200