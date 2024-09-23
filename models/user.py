# app/models/user.py
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    username: str = Field(..., max_length=50)
    email: EmailStr
    password_hash: str
    role: UserRole
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password_hash": "hashed_password",
                "role": "student",
                "created_at": "2023-01-01T00:00:00Z"
            }
        }




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str = None

class UserLogin(BaseModel):
    email: str
    password: str



class UserInfo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    username: str
    role: str
    link_id: UUID = Field(default_factory=uuid4)




class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: str

class TeacherResponse(BaseModel):
    id: UUID
    bio: Optional[str]
    location: Optional[str]
    expertise: str
    user: UserResponse  # Champ pour inclure les informations de l'utilisateur

    class Config:
        orm_mode = True