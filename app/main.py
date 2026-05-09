from fastapi import FastAPI

app = FastAPI(title="AI Message Persistence Service")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
