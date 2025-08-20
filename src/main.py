from fastapi import FastAPI
from controllers.bullens_chat_controller import router as chat_router

app = FastAPI()

app.include_router(
    chat_router,
    prefix="/bullens-chat",
    tags=["bullens-chat"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}