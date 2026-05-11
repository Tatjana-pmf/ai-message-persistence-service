# AI Message Persistence Service

REST API service for archiving messages exchanged between users and an AI assistant, persisted in PostgreSQL.

## Getting started

```
cp .env.example .env
docker-compose up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/messages` | Persist a new message |
| `PATCH` | `/messages/{message_id}` | Update an existing message |
| `GET` | `/messages` | Retrieve all messages |

## Database

PostgreSQL with SQLAlchemy ORM. Migrations managed by Alembic and run automatically on startup.
