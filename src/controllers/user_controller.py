from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select
from src.database import SessionDep
from passlib.context import CryptContext
from src.utils import create_access_token
from fastapi import APIRouter, HTTPException

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str = Field()
    id_used: Optional[bool] = Field(default=False, index=True)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginPayload(BaseModel):
    user_id: Optional[int] = None
    email: str
    password: str


@router.post('/user/create')
async def create_user(user: UserCreate, session: SessionDep):
    try:
        statement = select(User).where(User.email == user.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hash_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hash_password,
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {"message": "user created successfully!", "user_id": db_user.user_id}
    
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    

@router.post('/user/login')
async def login_user(Body: LoginPayload, session: SessionDep):
    
    try:
        user = session.get(User, Body.user_id)

        if not user:
          raise HTTPException(status_code=404, detail="User not found")
        
        if user.email != Body.email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        compared_password = pwd_context.verify(Body.password, user.password)

        if not compared_password:
            raise ValueError("Invalid password")
        
        if user.user_id is None:
            raise ValueError("Invalid user data")

        access_token = create_access_token(user.user_id)
        
        return {"message": "user login successful!", "token": access_token}
    
    except Exception as e:
        return {"error": str(e)}