from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware

import views
from app.dependencies import require_app_key
from app.exception_handlers import setup_exception_handlers
from app.logger import init_logging
from app.middlewares import check_app_key_middleware, logging_middleware

fastapi_params = {
    "title": "Cashbox Server",
    "description": "",
    "redoc_url": None,
    "docs_url": "/",
}


def create_app() -> FastAPI:
    init_logging()
    app = FastAPI(**fastapi_params)

    setup_exception_handlers(app)
    app.add_middleware(BaseHTTPMiddleware, dispatch=check_app_key_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

    app.include_router(views.websocket_routes)
    app.include_router(views.routes, dependencies=[Depends(require_app_key)])
    return app
