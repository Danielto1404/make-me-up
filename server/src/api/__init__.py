from fastapi import APIRouter

from .generation import router as generate_api

api = APIRouter(prefix="/api/v1")
api.include_router(generate_api)
