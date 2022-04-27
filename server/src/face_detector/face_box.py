from typing import Tuple, Union

import dlib
import numpy as np
from PIL import Image


class FaceBox:
    def __init__(
            self,
            image: Image,
            rect: Union[dlib.rectangle, Tuple[int, int, int, int]]
    ):

        self.image = image

        if isinstance(rect, dlib.rectangle):
            self.left = rect.left()
            self.right = rect.right()
            self.top = rect.top()
            self.bottom = rect.bottom()
        else:
            self.left, self.right, self.top, self.bottom = rect

    def paddings(self, px: int = 40, py: int = 180):
        w, h = self.image.size

        return FaceBox(
            image=self.image,
            rect=(
                max(0, self.left - px),
                min(w, self.right + px),
                max(0, self.top - py * 2),
                min(h, self.bottom + py)
            )
        )

    def crop(self) -> Image:
        array = np.asarray(self.image)
        cropped = array[self.top:self.bottom, self.left:self.right, :]
        return Image.fromarray(cropped)

    def __str__(self):
        return f"Box(left={self.left}, right={self.right}, top={self.top}, bottom={self.bottom})"

    __repr__ = __str__
