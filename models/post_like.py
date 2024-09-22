# app/models/post_like.py
from beanie import Document
from pydantic import Field
from uuid import UUID, uuid4


class PostLike(Document):
    id: UUID = Field(default_factory=uuid4)
    post_id: UUID
    user_id: UUID

    class Settings:
        collection = "post_likes"
