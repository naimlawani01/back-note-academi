# app/routes/user.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from models.user import Token, User, UserInfo, UserLogin, UserRole
from pydantic import BaseModel, EmailStr
from uuid import UUID
from utils.auth import create_access_token, decode_access_token, get_current_user, hash_password, verify_password, credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None



@router.get("/me", response_model=UserInfo)
async def get_info_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_access_token(token)  # Appel à la fonction utilitaire
    user = await User.get(UUID(user_id))
    
    if user is None:
        raise credentials_exception
    
    return UserInfo(
        id= user.id,
        email= user.email,
        username= user.username,
        role= user.role
    )

@router.post("/signup")
async def signup(user: UserCreate):
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    await new_user.insert()
    return {"message": "User created successfully", "user_id": new_user.id}


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdate):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.password:
        user_update.password_hash = hash_password(user_update.password)
    
    update_data = user_update.dict(exclude_unset=True, exclude={"password"})
    await user.set(update_data)
    
    return {"message": "User updated successfully"}


@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return {"message": "User deleted successfully"}


@router.post("/login", response_model=Token)
async def login(user_login: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.email == user_login.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}




