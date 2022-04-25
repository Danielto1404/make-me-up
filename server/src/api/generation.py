from fastapi import APIRouter, UploadFile, Depends
import torch
import torchvision
import time

from .dto import GenerateMakeRequestParams
from .utils import load_image_into_pil
from ..clip_trainer import CLIPTrainer
from ..depends import get_clip_trainer, get_ssat_model, get_face_parser
from ..faceparsing import FaceParser
from ..ssat import MakeupGAN, transfer as transfer_make
from .save_images import resize_source, resize_target, tensor2img
import matplotlib.pyplot as plt

router = APIRouter(prefix="/transfer")


@router.post("/")
async def transfer(
        img: UploadFile,
        params: GenerateMakeRequestParams = Depends(),
        clip_trainer: CLIPTrainer = Depends(get_clip_trainer),
        ssat: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    target = clip_trainer.train(
        prompts=params.prompts[0].split(','),
        initial_iterations=params.initial_iterations,
        iterations=params.iterations,
        truncation_psi=params.truncation_psi,
        batch_size=params.batch_size
    )
    
    torch.cuda.empty_cache()

    source = await load_image_into_pil(img)
    
    target = resize_target(target)
    source = resize_source(source)
    
    parser(target, './static/seg/makeup/target.png')
    parser(source, './static/seg/non-makeup/source.png')
    
    target.save('./static/images/makeup/target.png')
    source.save('./static/images/non-makeup/source.png')

    result = transfer_make(ssat)
    
    torchvision.utils.save_image(result / 2 + 0.5, f'save/{time.time()}.png', nrow=1)
