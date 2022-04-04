from fastapi import APIRouter

from .model import GenerateMakeRequestParams
from ..store import trainer

router = APIRouter(prefix="/generate")


@router.post("/")
async def generate_make(body: GenerateMakeRequestParams):
    latent = trainer.train(body)
    return latent
