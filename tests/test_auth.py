from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_manager():
    response = client.post(
        "/users",
        json={
            "name": "TestManager5",
            "password": "testpassword5"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "TestManager5"

def test_login_manager():
    response = client.post(
        "/login",
        json={
            "name": "TestManager5",
            "password": "testpassword5"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "TestManager5"

def test_login_wrong_password():
    response = client.post(
        "/login",
        json={
            "name": "TestManager5",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

def test_login_nonexistent_manager():
    response = client.post(
        "/login",
        json={
            "name": "DoesNotExist",
            "password": "testpassword5"
        }
    )

    assert response.status_code == 401