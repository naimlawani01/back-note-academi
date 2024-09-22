# app/routes/student.py
from fastapi import APIRouter, HTTPException
from models.student import Student
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class StudentProfileCreate(BaseModel):
    location: str = None

class StudentProfileUpdate(BaseModel):
    location: str = None


@router.post("/{user_id}/profile")
async def create_student_profile(user_id: UUID, profile: StudentProfileCreate):
    existing_student = await Student.find_one(Student.user_id == user_id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student profile already exists")
    
    student = Student(
        user_id=user_id,
        location=profile.location
    )
    await student.insert()
    return {"message": "Student profile created", "student_id": student.id}


@router.get("/{user_id}/profile", response_model=Student)
async def get_student_profile(user_id: UUID):
    student = await Student.find_one(Student.user_id == user_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


@router.put("/{user_id}/profile")
async def update_student_profile(user_id: UUID, profile_update: StudentProfileUpdate):
    student = await Student.find_one(Student.user_id == user_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    await student.set(update_data)
    
    return {"message": "Student profile updated successfully"}


@router.delete("/{user_id}/profile")
async def delete_student_profile(user_id: UUID):
    student = await Student.find_one(Student.user_id == user_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    await student.delete()
    return {"message": "Student profile deleted successfully"}
