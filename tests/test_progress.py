
import app.models as models

def test_add_and_get_progress(client, session):
    """full test progress of kanji model"""

    # 1. Создаем кандзи в тестовой БД
    kanji = models.Kanji(character="日", meaning="солнце")
    session.add(kanji)
    session.commit()
    session.refresh(kanji)
    kanji_id = kanji.id

    # 2. Регистрируем пользователя
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200 or response.status_code == 201

    # 3. Логинимся и получаем токен
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200 or login_response.status_code == 201

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Добавляем кандзи в прогресс (POST)
    post_progress = client.post(
        f"/api/v1/progress/kanji/{kanji_id}",
        headers=headers
    )

    print("STATUS:", post_progress.status_code)
    print("BODY:", post_progress.json())

    assert post_progress.status_code in (200, 201)
    data = post_progress.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    
    # 5. Проверяем список выученного (GET)
    get_response = client.get(
        "/api/v1/progress/kanji",
        headers=headers
    )
    assert get_response.status_code == 200 or get_response.status_code == 201
    data2 = get_response.json()
    assert isinstance(data2, list)
    assert len(data2) == 1
    assert data2[0]["character"] == "日"

    print("GET PROGRESS RESPONSE:", data2)