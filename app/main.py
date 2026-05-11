from fastapi import FastAPI

from app.api import messages

app = FastAPI(title="AI Message Persistence Service")
app.include_router(messages.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
