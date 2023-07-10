from starlette.requests import Request
from fastapi import Response


async def check_app_key_middleware(request: Request, call_next):
    if "app-key" in request.headers.keys():
        app_key = request.headers.get("app-key")
        if app_key != "admin":
            return Response(status_code=403)
    response = await call_next(request)
    return response