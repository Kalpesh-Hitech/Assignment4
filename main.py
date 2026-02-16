from fastapi import FastAPI
from database import Base,SessionLocal,engine
from routes import router
app=FastAPI()

app.include_router(router)
