import uvicorn
from fastapi import FastAPI
from app.app import create_app
from app.config_loader import config


app: FastAPI = create_app()

if __name__ == "__main__":
    uvicorn.run("asgi:app", host=config.SERVER_HOST, port=5000, log_level="debug", reload=True)
