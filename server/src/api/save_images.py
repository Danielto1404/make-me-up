from PIL import Image
import numpy as np


def resize(img, size=280):
    width, height = img.size

    new_height = size
    new_width = int(new_height * width / height)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return img


def embed_image_in_box(img, box_size):
    image_copy = np.asarray(img, np.uint8)
    box = np.zeros((box_size, box_size, 3))

    half = box_size // 2
    half_x, half_y = image_copy.shape[0] // 2, image_copy.shape[1] // 2

    bound = image_copy[:, :, :3]

    box[half - half_x: half + half_x, half - half_y: half + half_y, :] = bound
    return Image.fromarray(box.astype(np.uint8))


def resize_source(img):
    img = resize(img, 360)
    box = embed_image_in_box(img, 361)
    return box


def resize_target(img):
    img = resize(img, 290)
    box = embed_image_in_box(img, 361)
    return box
