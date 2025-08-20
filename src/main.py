from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import create_db_and_tables
from src.controllers import chat_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    chat_controller.router,
    prefix="/bullens",
    tags=["bullens-chat"])


@app.get("/")
async def root():
    return {"message": "Hello, World!"}