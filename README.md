# AI Message Persistence Service

REST API service for archiving messages exchanged between users and an AI assistant, persisted in PostgreSQL.

## Stack

- Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic
- PostgreSQL, Docker

## Getting started

```bash
cp .env.example .env
# fill in values in .env
docker-compose up --build
```

Migrations run automatically on startup. The API is available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

## Authentication

All `/messages` endpoints require a Bearer token. Get one via:

```
POST /token
```

Include it in subsequent requests:

```
Authorization: Bearer <token>
```

Tokens expire after 60 minutes.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/token` | Get an access token |
| `POST` | `/messages` | Persist a new message |
| `PATCH` | `/messages/{message_id}` | Update content or rating |
| `GET` | `/messages` | Retrieve all messages |

### Message fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `message_id` | UUID | yes | Set by the caller |
| `chat_id` | UUID | yes | Groups messages into a conversation |
| `content` | string | yes | Message text |
| `role` | `user` \| `ai` | yes | Who sent the message |
| `sent_at` | datetime | yes | Timestamp with timezone |
| `rating` | boolean | no | User feedback on AI response |

Only `content` and `rating` can be updated via PATCH.

## Running tests

Create the test database once (requires Docker running):

```bash
docker-compose exec postgres createdb -U postgres app_test
```

Run the test suite:

```bash
poetry run pytest
```
