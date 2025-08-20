from sqlmodel import SQLModel, Field
from src.database import SessionDep
from fastapi import APIRouter

router = APIRouter()

class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)


@router.post('/create/user')
async def create_user(user: User, session: SessionDep):
    return {"message": "User created successfully!"}