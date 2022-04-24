import matplotlib.pyplot as plt
from fastapi import APIRouter, UploadFile, Depends

from src.depends import get_face_parser, get_clip_trainer
from .utils import load_image_into_pil
from ..faceparsing import FaceParser
from ..clip_trainer.train import CLIPTrainer

router = APIRouter(prefix="/generate")


# @router.post("/")
# async def generate_make(body: GenerateMakeRequestParams):
#     latent = trainer.train(body)
#     return latent
#
#
# @router.get("/clip_trainer")
# async def t():
#     options = MakeOptions()
#     options.device = device
#     options.dataroot = '../SSAT/test/images'
#     clip_trainer(ssat_model, options)


@router.post("/parse")
async def parse(img: UploadFile, parser: FaceParser = Depends(get_face_parser)):
    image = await load_image_into_pil(img)
    rsult = parser(image)
    plt.imshow(rsult)
    plt.show()
    return 'ok'


@router.get('/')
async def clip(clip: CLIPTrainer = Depends(get_clip_trainer)):
    print(clip.device)
    return 'ok'
