from typing import List
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from fastapi import APIRouter
from src.database import SessionDep
from fastapi.responses import StreamingResponse
from src.agents.agent_chat import create_chat_agent

router = APIRouter()

class Chat(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    message: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    response: List[str] = Field(default_factory=list, sa_column=Column(JSON))

class ChatCreate(SQLModel):
    chat_id: str
    user_id: str
    message: str

async def stream_and_save(chat_message: str, session: SessionDep, chat: Chat):
    response_buffer = ''
    async for chunk in create_chat_agent(chat_message):
        response_buffer += chunk
        yield chunk

    if not isinstance(chat.response, list):
        chat.response = [chat.response.replace('\\', '')] if chat.response else []
        
    chat.response.append(response_buffer)
    session.add(chat)
    session.commit()
    session.refresh(chat)

@router.post('/chat/create')
async def create_chat(ChatArgs: ChatCreate, session: SessionDep):
    try:
        chat = session.get(Chat, ChatArgs.chat_id)
        if chat:
            if not isinstance(chat.message, list):
                chat.message = [chat.message] if chat.message else []
            chat.message.append(ChatArgs.message)
        else:
            chat = Chat(
                chat_id=ChatArgs.chat_id,
                user_id=ChatArgs.user_id,
                message=[ChatArgs.message],
                response=[]
            )
            session.add(chat)
        session.commit()
        session.refresh(chat)
        return StreamingResponse(stream_and_save(ChatArgs.message, session, chat), media_type="text/event-stream")
    except Exception as e:
        session.rollback()
        return {"error": str(e)}