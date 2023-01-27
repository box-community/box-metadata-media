# project/app/main.py

from fastapi import FastAPI
from app.api import info

def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(info.router)
    return application

app = create_application()
