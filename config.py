# app/config.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.teacher import Teacher
from models.student import Student
from models.message import Message
from models.post import Post
from models.post_like import PostLike
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://najathlawani73:QbJJXgG06MhCg02z@cluster0.4kgjy6f.mongodb.net")


async def init_db():
    CONNECTION_STRING = os.getenv('MONGO_URL')

    # Create a MongoDB client
    client = AsyncIOMotorClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    await init_beanie(database=client.social, document_models=[User, Teacher, Student, Message, Post, PostLike],)
