from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import MessageRole


class MessageCreate(BaseModel):
    message_id: UUID
    chat_id: UUID
    content: str
    rating: bool | None = None
    sent_at: datetime
    role: MessageRole


class MessageUpdate(BaseModel):
    content: str | None = None
    rating: bool | None = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: UUID
    chat_id: UUID
    content: str
    rating: bool | None
    sent_at: datetime
    role: MessageRole
