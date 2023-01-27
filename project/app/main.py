# project/app/main.py

from fastapi import FastAPI, Depends

from app.config import get_settings

app = FastAPI()


@app.get("/info")
async def get_server_info(settings = Depends(get_settings)):
    """Returns current service info and settings"""
    # TODO: Scrub sensitive settings
    return settings.dict()
