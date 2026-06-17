from fastapi.testclient import TestClient

from main import app, verify_user


client = TestClient(app)


def fake_verify_user():
    return True


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
    app.dependency_overrides[verify_user] = fake_verify_user

    response = client.get("/courses")

    app.dependency_overrides.clear()

    assert response.status_code == 200