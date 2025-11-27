from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


user = {
    "username": "test_user_simple",
    "password": "testpassword"
}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_register():
    response = client.post("/register", json=user)
    # Accept success OR "already exists"
    assert response.status_code in [200, 400]

def test_login():
    response = client.post("/login", json=user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    global token
    token = response.json()["access_token"]  # save token for next test

def test_translate_without_token():
    response = client.post("/translate", json={
        "text": "Bonjour",
        "source_language": "fr",
        "target_language": "en"
    })
    # Missing token → should be 422 (validation error)
    assert response.status_code == 422

def test_translate_with_invalid_token():
    response = client.post("/translate?token=wrongtoken123", json={
        "text": "Bonjour",
        "source_language": "fr",
        "target_language": "en"
    })
    # Should be unauthorized
    assert response.status_code in [401, 403]

def test_translate_with_valid_token():
    response = client.post(f"/translate?token={token}", json={
        "text": "Bonjour",
        "source_language": "fr",
        "target_language": "en"
    })

    assert response.status_code == 200
    data = response.json()
    # Translation key could vary
    assert "translated_text" in data 
