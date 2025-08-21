from sqlmodel import SQLModel, Field
from fastapi import APIRouter
from src.database import SessionDep
from fastapi.responses import StreamingResponse
from src.agents.agent_chat import create_chat_agent

router = APIRouter()


class Chat(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    message: str = Field(index=True)
    response: str = Field(default='')

async def stream_and_save(chat_message: str, session: SessionDep, chat: Chat):
    response_buffer = ''
    async for chunk in create_chat_agent(chat_message):
        response_buffer += chunk
        yield chunk

    chat.response = response_buffer
    session.add(chat)
    session.commit()
    session.refresh(chat)


@router.post('/chat/create')
async def create_chat(ChatArgs: Chat, session: SessionDep):
    chat = Chat(chat_id=ChatArgs.chat_id, user_id=ChatArgs.user_id, message=ChatArgs.message)
    session.add(chat)
    session.commit()
    session.refresh(chat)

    return StreamingResponse(stream_and_save(chat.message, session, chat), media_type="text/event-stream")