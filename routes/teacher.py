# app/routes/teacher.py
from fastapi import APIRouter, HTTPException
from models.teacher import Teacher
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class TeacherProfileCreate(BaseModel):
    bio: str = None
    location: str = None
    expertise: str

class TeacherProfileUpdate(BaseModel):
    bio: str = None
    location: str = None
    expertise: str = None


@router.post("/{user_id}/profile")
async def create_teacher_profile(user_id: UUID, profile: TeacherProfileCreate):
    existing_teacher = await Teacher.find_one(Teacher.user_id == user_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher profile already exists")
    
    teacher = Teacher(
        user_id=user_id,
        bio=profile.bio,
        location=profile.location,
        expertise=profile.expertise
    )
    await teacher.insert()
    return {"message": "Teacher profile created", "teacher_id": teacher.id}


@router.get("/{user_id}/profile", response_model=Teacher)
async def get_teacher_profile(user_id: UUID):
    teacher = await Teacher.find_one(Teacher.user_id == user_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return teacher


@router.put("/{user_id}/profile")
async def update_teacher_profile(user_id: UUID, profile_update: TeacherProfileUpdate):
    teacher = await Teacher.find_one(Teacher.user_id == user_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    await teacher.set(update_data)
    
    return {"message": "Teacher profile updated successfully"}


@router.delete("/{user_id}/profile")
async def delete_teacher_profile(user_id: UUID):
    teacher = await Teacher.find_one(Teacher.user_id == user_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    await teacher.delete()
    return {"message": "Teacher profile deleted successfully"}
