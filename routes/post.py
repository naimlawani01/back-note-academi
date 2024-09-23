# app/routes/post.py
from fastapi import APIRouter, HTTPException
from models.post import Post
from models.teacher import Teacher
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

router = APIRouter()

class PostCreate(BaseModel):
    teacher_id: UUID
    content: str
    media_url: str


@router.post("/create")
async def create_post(post: PostCreate):
    teacher = await Teacher.find_one(Teacher.id == post.teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    new_post = Post(
        teacher_id=post.teacher_id,
        content=post.content,
        media_url=post.media_url,
        created_at=datetime.utcnow()
    )
    await new_post.insert()
    return {"message": "Post created successfully", "post_id": new_post.id}


@router.get("/")
async def get_posts():
    posts = await Post.find_all().to_list()
    return posts


@router.delete("/{post_id}")
async def delete_post(post_id: UUID):
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await post.delete()
    return {"message": "Post deleted successfully"}
