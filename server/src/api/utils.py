import io

from PIL import Image
from fastapi import UploadFile


async def load_image_into_pil(image: UploadFile) -> Image:
    bytes_stream = await image.read()
    return Image.open(io.BytesIO(bytes_stream))
