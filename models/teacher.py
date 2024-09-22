# app/models/teacher.py
from beanie import Document
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Teacher(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    bio: str = None
    location: str = None
    expertise: str

    class Settings:
        collection = "teachers"
