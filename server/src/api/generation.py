import base64
import os

import cv2
import torch
import torchvision.utils
from PIL import Image
from fastapi import APIRouter, UploadFile, Depends, File, Form, HTTPException

from .save_images import resize_source, resize_target
from .validation import validate_source_face, validate_prompts, PromptsValidationError
from ..depends import get_ssat_model, get_face_parser
from ..face_detector import FaceDetectorError
from ..face_parsing import FaceParser
from ..image_utils import image_base64_encode
from ..ssat import MakeupGAN, transfer as transfer_make

router = APIRouter(prefix="/transfer")


@router.post("/")
async def transfer(
        file: UploadFile = File(...),
        prompts: str = Form(...),
        # clip_trainer: CLIPTrainer = Depends(get_clip_trainer),
        transfer_model: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    try:
        source = await validate_source_face(file)
        prompts = validate_prompts(prompts)

        # target = clip_trainer.train(
        #     prompts=prompts,
        #     initial_iterations=2,
        #     iterations=32,
        #     truncation_psi=0.75,
        #     batch_size=4
        # )

        target = Image.open("../../../Downloads/0006.png")

        torch.cuda.empty_cache()

        target = resize_target(target)
        source = resize_source(source)
        target_parsing = parser(target)
        source_parsing = parser(source)

        result = transfer_make(transfer_model, source, target, source_parsing, target_parsing).cpu().squeeze(0)
        result = result / 2 + 0.5

        return {
            "status_code": 200,
            "base64_image": image_base64_encode(result)
        }

    except FaceDetectorError as e:
        print(e)
        return HTTPException(status_code=422, detail=str(e))

    except PromptsValidationError as e:
        print(e)
        return HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
