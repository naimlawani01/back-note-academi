# app/models/student.py
from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4


class Student(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    location: str = None

    class Settings:
        collection = "students"
