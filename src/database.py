import os
from fastapi import Depends
from typing import Annotated
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

DEV_DB_URL = os.getenv("DEV_DB_URL")

if not DEV_DB_URL:
    raise ValueError("DEV_DB_URL environment variable is not set.")

engine = create_engine(DEV_DB_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]