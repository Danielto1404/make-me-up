from fastapi import APIRouter

from .auth import router as auth_api
from .generation import router as generate_api
from .user import router as user_api

api = APIRouter(prefix="/api/v1")
api.include_router(auth_api, tags=["Authorization"])
api.include_router(user_api, tags=["Users"])
api.include_router(generate_api, tags=["Deep Learning models"])
