import os

import numpy as np
from PIL import Image

import cv2


def save_images(
        source: Image,
        target: Image,
        source_parsing: np.ndarray,
        target_parsing: np.ndarray
):

    os.makedirs('./static/images/makeup', exist_ok=True)
    os.makedirs('./static/images/non-makeup', exist_ok=True)
    os.makedirs('./static/seg/makeup', exist_ok=True)
    os.makedirs('./static/seg/non-makeup', exist_ok=True)

    target.save('./static/images/makeup/target.png')
    source.save('./static/images/non-makeup/source.png')

    cv2.imwrite('./static/seg/makeup/target.png', target_parsing)
    cv2.imwrite('./static/seg/non-makeup/source.png', source_parsing)
