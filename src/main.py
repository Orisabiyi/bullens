from fastapi import FastAPI
from src.database import create_db_and_tables
from src.controllers import chat_controller


app = FastAPI()

app.include_router(
    chat_controller.router,
    prefix="/bullens",
    tags=["bullens-chat"])


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}