import dlib
import numpy as np
from PIL import Image

from .error import FaceDetectorError
from .face_box import FaceBox


class FaceDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def detect(self, image: Image, upsample=3) -> FaceBox:
        """
        Detects one face.
        If no faces found or found multiple faces then `FaceDetectorError` will be raised.
        """
        _gray = np.asarray(image.convert("L"))
        faces = self.detector(_gray, upsample)
        boxes = [FaceBox(image, face_rect) for face_rect in faces]

        if len(boxes) == 0:
            raise FaceDetectorError("No face found on image")
        if len(boxes) >= 2:
            raise FaceDetectorError(f"Only one face should be on image, but found {len(boxes)}")

        face = boxes[0]

        return face

    def __call__(self, image: Image, upsample=3) -> FaceBox:
        """
        Wrapper of `detect` method
        """
        return self.detect(image, upsample)
