from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_access_token(user_id: int) -> str:
    to_encode = {"user_id": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=60)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt