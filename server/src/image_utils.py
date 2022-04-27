import base64
import io
import os

import cv2
import numpy as np
import torch
import torchvision.utils
from PIL import Image


def resize_with_aspect(
        image: np.ndarray,
        size: int = 512
) -> np.ndarray:
    h, w, c = image.shape
    resized = np.zeros((size, size, c))

    scale = size / max(h, w)

    image = cv2.resize(image, (int(scale * w), int(scale * h)), interpolation=cv2.INTER_NEAREST)

    nh, nw, _ = image.shape
    px, py = (size - nw) // 2, (size - nh) // 2

    resized[py:py + nh, px:px + nw, :] = image

    return resized


def image_base64_encode(tensor: torch.Tensor):
    os.makedirs('./generated', exist_ok=True)
    torchvision.utils.save_image(tensor, './generated/result.png')

    image = Image.open('./generated/result.png')

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")
