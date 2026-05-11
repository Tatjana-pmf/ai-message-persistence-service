from fastapi import FastAPI

from app.api import messages
from app.core.security import create_access_token

app = FastAPI(title="AI Message Persistence Service")
app.include_router(messages.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/token")
def get_token() -> dict:
    return {"access_token": create_access_token(), "token_type": "bearer"}
