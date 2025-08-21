from typing import Optional
from sqlmodel import SQLModel, Field
from src.database import SessionDep
from passlib.context import CryptContext
from fastapi import APIRouter

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field()


@router.post('/create/user')
async def create_user(user: User, session: SessionDep):
    try:
        hash_password = pwd_context.hash(user.password)
        user.password = hash_password
        
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "User created successfully!", "user_id": user.user_id}
    
    except Exception as e:
        session.rollback()
        return {"error": str(e)}