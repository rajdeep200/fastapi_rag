from sqlalchemy import select

from app.models.user import User


def register(client, email="alice@example.com", password="password123", name="Alice", age=25):
    return client.post(
        "/auth/register",
        json={"name": name, "email": email, "age": age, "password": password},
    )


def login(client, email="alice@example.com", password="password123"):
    return client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )


def test_register_success(client):
    response = register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_email_returns_409(client):
    register(client)
    response = register(client)

    assert response.status_code == 409


def test_register_invalid_email_returns_422(client):
    response = register(client, email="not-an-email")

    assert response.status_code == 422


def test_login_wrong_password_returns_401(client):
    register(client)
    response = login(client, password="wrong-password")

    assert response.status_code == 401


def test_login_success_returns_token(client):
    register(client)
    response = login(client)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_me_with_token_returns_current_user(client):
    register(client)
    token = login(client).json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


def test_users_without_token_returns_401(client):
    response = client.get("/users/")

    assert response.status_code == 401


def test_update_own_account_returns_200(client):
    user_id = register(client).json()["id"]
    token = login(client).json()["access_token"]

    response = client.put(
        f"/users/{user_id}",
        json={"name": "Alice Updated"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"


def test_delete_other_users_account_returns_403(client):
    register(client, email="alice@example.com")
    other_id = register(client, email="bob@example.com").json()["id"]
    token = login(client, email="alice@example.com").json()["access_token"]

    response = client.delete(
        f"/users/{other_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_stored_password_is_hashed(client, db_session):
    register(client, password="password123")

    user = db_session.scalar(select(User).where(User.email == "alice@example.com"))

    assert user.hashed_password != "password123"
    assert user.hashed_password.startswith("$argon2")
