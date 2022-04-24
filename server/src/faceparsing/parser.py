import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from PIL.Image import Resampling

from .model import BiSeNet


class FaceParser:
    def __init__(self, model_path: str, device: str = 'cpu'):
        self.model_path = model_path
        self.device = device

        self.classes = 19

        self.net = FaceParser \
            .setup_model(self.classes, model_path, map_location=device) \
            .to(device) \
            .eval()

        self.to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

    @staticmethod
    def setup_model(n_classes, model_path, map_location=None):
        state = torch.load(model_path, map_location=map_location)

        net = BiSeNet(n_classes=n_classes)
        net.load_state_dict(state)

        return net

    @torch.no_grad()
    def evaluate(self, image: Image, resize=(512, 512)) -> Image:
        image = image.resize(resize, Resampling.BILINEAR)
        image = self.to_tensor(image)
        image = torch.unsqueeze(image, 0)
        image = image.to(self.device)

        out = self.net(image)[0]
        parsing = out \
            .squeeze(0) \
            .cpu() \
            .numpy() \
            .argmax(0) \
            .astype(np.int8)

        return Image.fromarray(parsing)

    __call__ = evaluate