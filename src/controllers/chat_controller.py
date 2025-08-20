from sqlmodel import SQLModel, Field
from fastapi import APIRouter
from src.database import SessionDep

router = APIRouter()


class Chat(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    message: str = Field(index=True)


@router.post('/create/chat')
async def create_chat(ChatArgs: Chat, session: SessionDep):
    return {"message": "Chat created successfully!"}