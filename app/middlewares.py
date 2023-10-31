from starlette.requests import Request
from fastapi import Response

from app.config_loader import config
from app.logger import logger


async def check_app_key_middleware(request: Request, call_next):
    if "app-key" in request.headers.keys():
        app_key = request.headers.get("app-key")
        if app_key != config.APP_KEY:
            return Response(status_code=403)
    response = await call_next(request)
    return response


async def logging_middleware(request: Request, call_next):
    logger.info("REQUEST " + request.method + " -> " + str(request.url))
    response = await call_next(request)
    return response
