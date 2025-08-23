import json
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
    user_id: int = Field(index=True, foreign_key="user.user_id")
    message: List[str] = Field(sa_column=Column(JSON), default=[])
    response: List[str] = Field(sa_column=Column(JSON), default=[])

class ChatCreate(SQLModel):
    chat_id: str
    user_id: int
    message: str

async def stream_and_save(chat_message: str, session: SessionDep, chat: Chat):
    response_buffer = ''
    chat_response = json.loads(chat.response) if type(chat.response) == str else chat.response

    async for chunk in create_chat_agent(chat_message):
        response_buffer += chunk
        yield chunk

    if not type(chat_response) == list and (not chat_response or chat_response == []):
        chat.response = [response_buffer]
    else:
        chat_response.append(response_buffer)
        chat.response = chat_response

    session.add(chat)
    session.commit()
    session.refresh(chat)


@router.post('/chat/create')
async def create_chat(ChatArgs: ChatCreate, session: SessionDep):
    try:
        chat = session.get(Chat, ChatArgs.chat_id)
        chat_data = json.loads(chat.message) if chat and type(chat.message) == str else []

        if chat:
            chat_data.append(ChatArgs.message)
            chat.message = chat_data
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