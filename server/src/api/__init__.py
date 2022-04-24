from fastapi import APIRouter

from .auth import router as auth_api
from .generation import router as generate_api

api = APIRouter(prefix="/api/v1")
api.include_router(auth_api)
api.include_router(generate_api)
