def test_register_user(client):
    response = client.post(
        "/auth/register", json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code in (200, 400)


def test_login(client):
    client.post("/auth/register", json={"username": "admin", "password": "admin123"})
    response = client.post(
        "/auth/token", data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
