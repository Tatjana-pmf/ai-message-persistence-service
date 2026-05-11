from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Message
from app.schemas import MessageCreate, MessageResponse, MessageUpdate

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[MessageResponse])
def get_messages(db: Session = Depends(get_db)) -> list[Message]:
    return list(db.execute(select(Message)).scalars().all())


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(data: MessageCreate, db: Session = Depends(get_db)) -> Message:
    if db.get(Message, data.message_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Message {data.message_id} already exists"
        )
    message = Message(**data.model_dump(exclude_none=True))
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.patch("/{message_id}", response_model=MessageResponse)
def update_message(message_id: UUID, data: MessageUpdate, db: Session = Depends(get_db)) -> Message:
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message {message_id} not found"
        )
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(message, field, value)
    db.commit()
    db.refresh(message)
    return message
