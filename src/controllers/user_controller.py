from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from src.database import SessionDep
from passlib.context import CryptContext
from src.utils import create_access_token
from fastapi import APIRouter

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field()
    id_used: Optional[bool] = Field(default=None, index=True)


class LoginPayload(BaseModel):
    user_id: Optional[int] = None
    email: str
    password: str


@router.post('/user/create')
async def create_user(user: User, session: SessionDep):
    try:
        hash_password = pwd_context.hash(user.password)
        user.password = hash_password

        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "user created successfully!", "user_id": user.user_id}
    
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    

@router.post('/user/login')
async def login_user(Body: LoginPayload, session: SessionDep):
    
    try:
        user = session.get(User, Body.email)

        if not user:
          raise ValueError("User not found")
        
        compared_password = pwd_context.verify(Body.password, user.password)

        if not compared_password:
            raise ValueError("Invalid password")
        
        if user.user_id is None:
            raise ValueError("Invalid user data")

        access_token = create_access_token(user.user_id)
        
        return {"message": "user login successful!", "token": access_token}
    
    except Exception as e:
        return {"error": str(e)}