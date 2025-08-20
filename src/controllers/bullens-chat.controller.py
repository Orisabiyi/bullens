from main import app
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    message: str

@app.post('/create/chat')
async def create_chat():
    return {"message": "Chat created successfully!"}