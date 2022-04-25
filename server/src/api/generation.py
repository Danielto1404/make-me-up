from fastapi import APIRouter, UploadFile, Depends

from .dto import GenerateMakeRequestParams
from .utils import load_image_into_pil
from ..clip_trainer import CLIPTrainer
from ..depends import get_clip_trainer, get_ssat_model, get_face_parser
from ..faceparsing import FaceParser
from ..ssat import MakeupGAN, transfer as transfer_make

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

    source = await load_image_into_pil(img)

    target_parse_result = parser(target)
    source_parse_result = parser(source)

    target.save('/image/makeup/target.png')
    source.save('/image/non-makeup/source.png')

    target_parse_result.save('./static/seg/makeup/target.png')
    source_parse_result.save('./static/seg/non-makeup/source.png')

    a, b = transfer_make(ssat)
