import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api import messages
from app.core.config import settings
from app.core.security import create_access_token

app = FastAPI(title="AI Message Persistence Service")
app.include_router(messages.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    username_ok = secrets.compare_digest(form_data.username, settings.api_username)
    password_ok = secrets.compare_digest(form_data.password, settings.api_password)
    if not username_ok or not password_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(), "token_type": "bearer"}
