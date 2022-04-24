from fastapi import APIRouter, UploadFile, Depends

from src.depends import get_face_parser, get_clip_trainer, get_ssat_model
from .dto import GenerateMakeRequestParams
from .utils import load_image_into_pil
from ..clip_trainer.train import CLIPTrainer
from ..faceparsing import FaceParser
from ..ssat import MakeupGAN

router = APIRouter(prefix="/transfer")


@router.post("/")
async def transfer(
        img: UploadFile,
        params: GenerateMakeRequestParams,
        clip_trainer: CLIPTrainer = Depends(get_clip_trainer),
        ssat: MakeupGAN = Depends(get_ssat_model),
        parser: FaceParser = Depends(get_face_parser)
):
    target = clip_trainer.train(
        prompts=params.prompts,
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
    plt.imshow(a)
    plt.show()
