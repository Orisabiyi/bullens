from fastapi import FastAPI
from src.controllers import chat_controller


app = FastAPI()

app.include_router(
    chat_controller.router,
    prefix="/bullens",
    tags=["bullens-chat"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}