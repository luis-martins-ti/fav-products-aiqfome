def test_create_client(client, auth_headers):
    response = client.post(
        "/clients/",
        json={"name": "João", "email": "teste@mail.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "João"


def test_get_all_clients(client, auth_headers):
    response = client.get("/clients/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


def test_update_client(client, auth_headers):
    response = client.post(
        "/clients/",
        json={"name": "Carlos", "email": "teste@teste.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    client_id = response.json()["id"]

    response = client.put(
        f"/clients/{client_id}",
        json={"name": "Carlos Silva", "email": "teste2@update.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Carlos Silva"


def test_delete_client(client, auth_headers):
    response = client.post(
        "/clients/",
        json={"name": "Delete Me", "email": "teste@delete.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    client_id = response.json()["id"]

    response = client.delete(
        f"/clients/{client_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204

    response = client.get("/clients/", headers=auth_headers)
    data = response.json()
    assert all(p["id"] != client_id for p in data["data"])
