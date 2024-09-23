# app/routes/teacher.py
from typing import List
from fastapi import APIRouter, HTTPException
from models.teacher import Teacher
from pydantic import BaseModel
from uuid import UUID

from models.user import TeacherResponse, User, UserResponse

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




@router.get("/top_teachers", response_model=List[TeacherResponse])
async def get_top_teachers():
    # Récupère les 10 premiers professeurs triés par date de création
    teachers = await Teacher.find().sort("-created_at").limit(10).to_list()
    
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found")
    
    teacher_responses = []
    
    # Parcours chaque professeur et récupère les informations de l'utilisateur associé
    for teacher in teachers:
        user = await User.get(teacher.user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User associated with teacher {teacher.id} not found")
        
        # Crée une réponse combinée des informations du professeur et de l'utilisateur
        teacher_responses.append(
            TeacherResponse(
                id=teacher.id,
                bio=teacher.bio,
                location=teacher.location,
                expertise=teacher.expertise,
                user=UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    role=user.role,
                )
            )
        )
    
    return teacher_responses