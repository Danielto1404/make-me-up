from PIL import Image
import numpy as np


def resize(img: Image, size=280) -> Image:
    width, height = img.size

    new_height = size
    new_width = int(new_height * width / height)

    img = img.resize((new_width, new_height), Image.BILINEAR)
    return img


def apply_paddings(img: Image, padding: int) -> Image:
    image_copy = np.asarray(img, np.uint8)
    h, w, c = image_copy.shape
    box = np.zeros((h + 2 * padding, w + 2 * padding, min(c, 3)))

    box[padding: padding + h, padding: padding + w, :] = image_copy[:, :, :3]
    return box


def resize_source(img: Image) -> np.ndarray:
    img = resize(img, 512)
    box = apply_paddings(img, 0)
    return box


def resize_target(img: Image) -> np.ndarray:
    img = resize(img, 512)
    box = apply_paddings(img, 50)
    return box
