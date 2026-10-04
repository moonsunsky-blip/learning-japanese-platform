

def test_reegister_user(client):
    """тест успешной авторизации"""
    response = client.post(
        "/api/v1/auth/register",
        json = {"email": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicat_email(client):
    """тест ошиби при регистрации двух пользователей"""

    client.post(
        "/api/v1/auth/register",
        json = {"email": "test@example.com", "password": "password123"}
    )

    response = client.post(
        "/api/v1/auth/register",
            json = {"email": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"

def test_login(client):
    """test user jwt token"""

    client.post(
        "/api/v1/auth/register",
        json = {"email": "test@example.com", "password": "password123"}
    )

    response = client.post(
        "/api/v1/auth/login",
        data = {"username": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] 
    assert data["token_type"] == "bearer"