import time
from typing import List

import torch
import torchvision
from fastapi import APIRouter, UploadFile, Depends, File, Form, HTTPException
from starlette.responses import FileResponse, Response

from .dto import GenerateMakeRequestParams
from .save_images import resize_source, resize_target
from .utils import load_image_into_pil
from ..clip_trainer import CLIPTrainer
from ..depends import get_clip_trainer, get_ssat_model, get_face_parser
from ..faceparsing import FaceParser
from ..ssat import MakeupGAN, transfer as transfer_make

router = APIRouter(prefix="/transfer")


@router.post("/")
async def transfer(
        file: UploadFile = File(...),
        prompts: str = Form(...),
        params: GenerateMakeRequestParams = Depends(),
        clip_trainer: CLIPTrainer = Depends(get_clip_trainer),
        ssat: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    try:
        target_prompts = prompts.split("|")
        if len(target_prompts) == 0:
            raise HTTPException(status_code=404, detail="No prompts provided")
        if len(target_prompts) > 3:
            raise HTTPException(status_code=404, detail="Given too much prompts. Maximum amount of prompt is 3")

        target = clip_trainer.train(
            prompts=params.prompts[0].split(','),
            initial_iterations=params.initial_iterations,
            iterations=params.iterations,
            truncation_psi=params.truncation_psi,
            batch_size=params.batch_size
        )

        torch.cuda.empty_cache()

        source = await load_image_into_pil(file)

        target = resize_target(target)
        source = resize_source(source)

        parser(target, './static/seg/makeup/target.png')
        parser(source, './static/seg/non-makeup/source.png')

        target.save('./static/images/makeup/target.png')
        source.save('./static/images/non-makeup/source.png')

        result = transfer_make(ssat)

        torchvision.utils.save_image(result / 2 + 0.5, './save/generated.png', nrow=1)

        return FileResponse(path='./save/generated.png', media_type='image/png')

    except Exception:
        raise HTTPException(status_code=404, detail="Invalid params")
