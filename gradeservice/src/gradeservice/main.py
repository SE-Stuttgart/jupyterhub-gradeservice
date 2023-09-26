import os
import sys

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import authorization_middleware
from .config import settings
from .otter import router

# Check if the assignments path exists and is readable/writeable.
# Defaults to current working dir if ASSIGNMENTS_PATH environment variable is not set.
settings.assignments_path = settings.assignments_path.resolve()

print(f'"{settings.assignments_path}"')
if not settings.assignments_path.is_dir():
    print(f'The directory "{settings.assignments_path}" doesnt exist!')
    sys.exit()

if not os.access(settings.assignments_path, os.W_OK) or not os.access(
    settings.assignments_path, os.R_OK
):
    print(f'No read/write acces in directory "{settings.assignments_path}"!')
    sys.exit()

if (not settings.no_auth) and settings.jwt_secret == "":
    print("No jwt secret set!")
    sys.exit()

app = FastAPI()

if not settings.no_auth:
    app.add_middleware(BaseHTTPMiddleware, dispatch=authorization_middleware)

app.include_router(router)
