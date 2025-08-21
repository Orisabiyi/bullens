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
    chat = Chat(chat_id=ChatArgs.chat_id, user_id=ChatArgs.user_id, message=ChatArgs.message)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return {"message": "Chat created successfully!"}