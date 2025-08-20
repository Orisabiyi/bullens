from sqlmodel import SQLModel, Field, create_engine
from fastapi import APIRouter

router = APIRouter()

class User(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)


@router.post('/create/user')
async def create_user(user: User):
    return {"message": "User created successfully!"}