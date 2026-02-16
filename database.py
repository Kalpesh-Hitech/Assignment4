from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import HTTPException

if DATABASE_URL is None:
    raise HTTPException(status_code=404, detail="url is not defined!!")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
