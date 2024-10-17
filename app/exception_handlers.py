import json

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import WebSocketException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.websockets import WebSocketClose

from .exceptions import AppError, ValidationError, ErrorMessages
from .logger import logger


class ASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logger.error(f"Unhandled error: {exc!r}", exc_info=True)

            # Обработка WebSocket исключений
            if scope["type"] == "websocket":
                exc: WebSocketException
                resp = WebSocketClose(code=1000)  # 1000 - код закрытия WebSocket
                await resp(scope, receive, send)

            # Обработка HTTP исключений
            elif scope["type"] == "http":
                # Отправляем заголовки ответа
                await send({
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [
                        (b"content-type", b"application/json"),
                    ]
                })

                # Отправляем тело ответа с ошибкой в формате JSON
                await send({
                    "type": "http.response.body",
                    "body": json.dumps({"error": ErrorMessages.DEFAULT_MESSAGE.value}).encode(),
                    "more_body": False
                })


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    if exc.log:
        logger.error(repr(exc), exc_info=exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.get_data()),
        headers=exc.headers,
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    exc = ValidationError(detail=exc.errors())
    return await app_error_handler(request, exc)


EXCEPTION_HANDLERS = {
    AppError: app_error_handler,
    RequestValidationError: request_validation_exception_handler,
}


def setup_exception_handlers(app: FastAPI) -> None:
    for exc, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exc, handler)

    # Использовать хендлер для кода 500 или Exception класса нельзя, тк в таком случае
    # request_id middleware будет пропущено при поднятии исключения.
    # Поэтому для отлова исключений используется свое middleware,
    # которое должно отрабатывать до request_id middleware.

    app.add_middleware(ASGIMiddleware)
