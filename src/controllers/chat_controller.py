import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session
from fastapi import APIRouter

load_dotenv()

router = APIRouter()

DEV_DB_URL = os.getenv("DEV_DB_URL")

if not DEV_DB_URL:
    raise ValueError("DEV_DB_URL environment variable is not set.")


class Chat(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    message: str = Field(index=True)


@router.post('/create/chat')
async def create_chat(ChatArgs: Chat):
    return {"message": "Chat created successfully!"}