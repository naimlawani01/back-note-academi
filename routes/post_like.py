# app/routes/post_like.py
from fastapi import APIRouter, HTTPException
from models.post_like import PostLike
from models.post import Post
from models.user import User
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class LikeCreate(BaseModel):
    post_id: UUID
    user_id: UUID


@router.post("/like")
async def like_post(like: LikeCreate):
    post = await Post.get(like.post_id)
    user = await User.get(like.user_id)
    
    if not post or not user:
        raise HTTPException(status_code=404, detail="Post or user not found")
    
    existing_like = await PostLike.find_one(PostLike.post_id == like.post_id, PostLike.user_id == like.user_id)
    if existing_like:
        raise HTTPException(status_code=400, detail="User already liked this post")
    
    new_like = PostLike(
        post_id=like.post_id,
        user_id=like.user_id
    )
    await new_like.insert()
    return {"message": "Post liked successfully", "like_id": new_like.id}


@router.delete("/unlike")
async def unlike_post(like: LikeCreate):
    post_like = await PostLike.find_one(PostLike.post_id == like.post_id, PostLike.user_id == like.user_id)
    
    if not post_like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    await post_like.delete()
    return {"message": "Post unliked successfully"}
