# app/models/post.py
from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime


class Post(Document):
    id: UUID = Field(default_factory=uuid4)
    teacher_id: UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "posts"
