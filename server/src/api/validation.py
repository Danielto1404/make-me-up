import io
from typing import List

from PIL import Image
from fastapi import UploadFile, HTTPException

from src.face_detector import FaceDetector


async def load_image_into_pil(image: UploadFile) -> Image:
    bytes_stream = await image.read()
    return Image.open(io.BytesIO(bytes_stream))


class PromptsValidationError(Exception):
    def __init__(self, message):
        super(PromptsValidationError, self).__init__(message)


async def validate_source_face(file: UploadFile) -> Image:
    """
    Validates source image.

    Raises FaceDetectorError if an error occurred.
    """
    detector = FaceDetector()
    source = await load_image_into_pil(file)
    return detector(source).paddings().crop()


def validate_prompts(prompts: str) -> List[str]:
    """
    Validates target prompts.

    Raises HTTPException if prompts is invalid.
    """
    if not isinstance(prompts, str):
        raise PromptsValidationError("Prompts must be a string value")

    prompts = prompts.split("|")

    if len(prompts) == 0:
        raise PromptsValidationError("No prompts provided")
    if len(prompts) > 3:
        raise PromptsValidationError("Given too much prompts. Maximum amount of prompt is 3")

    return prompts
