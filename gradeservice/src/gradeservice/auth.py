import jwt
from fastapi import Request
from fastapi.responses import JSONResponse

from .config import settings


async def authorization_middleware(
    request: Request,
    call_next,
):
    if "Authorization" not in request.headers:
        return JSONResponse(status_code=401, content={"detail": "No authorization header"})

    if authorize(request.headers["Authorization"]):
        response = await call_next(request)
        return response

    return JSONResponse(status_code=401, content={"message": "Invalid token."})


def authorize(token: str) -> bool:
    try:
        jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return True
    except jwt.exceptions.InvalidTokenError:
        return False
