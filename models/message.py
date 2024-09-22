# app/models/message.py
from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime


class Message(Document):
    id: UUID = Field(default_factory=uuid4)
    sender_id: UUID
    receiver_id: UUID
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)

    class Settings:
        collection = "messages"
