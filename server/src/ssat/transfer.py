import torch
from PIL import Image

from .dataset import MakeupTransferData
from .model import MakeupGAN
from ..face_parsing import FaceParser
from ..image_utils import resize_target, resize_source


@torch.no_grad()
def transfer(
        ssat_model: MakeupGAN,
        face_parser: FaceParser,
        source: Image,
        target: Image,
) -> torch.Tensor:
    target = resize_target(target)
    source = resize_source(source)
    target_parsing = face_parser(target)
    source_parsing = face_parser(source)

    data = MakeupTransferData(source, target, source_parsing, target_parsing).get()
    result = ssat_model.test_pair(data).cpu()[0]
    result = result / 2 + 0.5

    return result
