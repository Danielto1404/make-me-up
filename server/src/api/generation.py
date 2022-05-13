import torch
from fastapi import APIRouter, UploadFile, Depends, File, Form, HTTPException

from .validation import validate_source_face, validate_prompts, PromptsValidationError
from ..clip_trainer import CLIPTrainer
from ..depends import get_ssat_model, get_face_parser, get_clip_trainer, get_stylegan_generator
from ..face_detector import FaceDetectorError
from ..face_parsing import FaceParser
from ..image_utils import image_base64_encode
from ..ssat import MakeupGAN, transfer as transfer_make
from ..stylegan import StyleganGenerator

router = APIRouter(prefix="/transfer")


@router.post("/")
async def transfer(
        file: UploadFile = File(...),
        prompts: str = Form(...),
        clip_trainer: CLIPTrainer = Depends(get_clip_trainer),
        transfer_model: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    try:
        source = await validate_source_face(file)
        prompts = validate_prompts(prompts)

        target = clip_trainer.train(
            prompts=prompts,
            initial_iterations=16,
            iterations=32,
            truncation_psi=0.8,
            batch_size=4
        )

        torch.cuda.empty_cache()

        result = transfer_make(transfer_model, parser, source, target)

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


@router.post("/random")
async def transfer(
        file: UploadFile = File(...),
        generator: StyleganGenerator = Depends(get_stylegan_generator),
        transfer_model: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    try:
        source = await validate_source_face(file)
        target = generator.gen_image()
        result = transfer_make(transfer_model, parser, source, target)

        return {
            "status_code": 200,
            "base64_image": image_base64_encode(result)
        }

    except FaceDetectorError as e:
        print(e)
        return HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
