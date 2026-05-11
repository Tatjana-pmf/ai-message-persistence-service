import uuid
from datetime import datetime, timezone


def make_message(**overrides) -> dict:
    base = {
        "message_id": str(uuid.uuid4()),
        "chat_id": str(uuid.uuid4()),
        "content": "Hello, world!",
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "role": "user",
    }
    return {**base, **overrides}


def test_get_messages_returns_empty_list(client, auth_headers):
    response = client.get("/messages", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_messages_unauthorized(client):
    response = client.get("/messages")
    assert response.status_code == 403


def test_create_message(client, auth_headers):
    message = make_message()
    response = client.post("/messages", json=message, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["message_id"] == message["message_id"]
    assert data["chat_id"] == message["chat_id"]
    assert data["content"] == message["content"]
    assert data["role"] == message["role"]
    assert data["sent_at"] is not None
    assert data["rating"] is None


def test_create_message_returns_409_on_duplicate(client, auth_headers):
    message = make_message()
    client.post("/messages", json=message, headers=auth_headers)
    response = client.post("/messages", json=message, headers=auth_headers)
    assert response.status_code == 409


def test_create_message_unauthorized(client):
    response = client.post("/messages", json=make_message())
    assert response.status_code == 403


def test_update_message_content(client, auth_headers):
    message = make_message()
    client.post("/messages", json=message, headers=auth_headers)
    response = client.patch(
        f"/messages/{message['message_id']}",
        json={"content": "Updated content"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Updated content"


def test_update_message_rating(client, auth_headers):
    message = make_message()
    client.post("/messages", json=message, headers=auth_headers)
    response = client.patch(
        f"/messages/{message['message_id']}",
        json={"rating": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["rating"] is True


def test_update_message_returns_404_when_not_found(client, auth_headers):
    response = client.patch(
        f"/messages/{uuid.uuid4()}",
        json={"content": "Updated"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_update_message_unauthorized(client):
    response = client.patch(f"/messages/{uuid.uuid4()}", json={"content": "Updated"})
    assert response.status_code == 403


def test_get_messages_returns_created_messages(client, auth_headers):
    message1 = make_message(content="First")
    message2 = make_message(content="Second")
    client.post("/messages", json=message1, headers=auth_headers)
    client.post("/messages", json=message2, headers=auth_headers)
    response = client.get("/messages", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
