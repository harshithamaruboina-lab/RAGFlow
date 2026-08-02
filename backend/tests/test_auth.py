def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "newuser@example.com"
    assert "hashed_password" not in body


def test_register_duplicate_email_fails(client):
    payload = {"email": "dupe@example.com", "password": "StrongPass123!"}
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 400


def test_login_success(client):
    email = "loginuser@example.com"
    password = "StrongPass123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    response = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password_fails(client):
    email = "badlogin@example.com"
    password = "StrongPass123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    response = client.post(
        "/api/v1/auth/login", data={"username": email, "password": "WrongPassword!"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user_fails(client):
    response = client.post(
        "/api/v1/auth/login", data={"username": "ghost@example.com", "password": "whatever"}
    )
    assert response.status_code == 401