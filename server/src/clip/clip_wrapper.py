import torch

from .clip import load as load_clip, tokenize as clip_tokenize
from ..utils import imagenet_normalize, norm1


class CLIP(object):
    def __init__(self, model_name, device):
        self.model_name = model_name
        self.device = device

        self.model, _ = load_clip(model_name)
        self.model = self.model.requires_grad_(False).to(device)
        self.normalize = imagenet_normalize

    @torch.no_grad()
    def embed_text(self, prompt) -> torch.Tensor:
        """Normalized clip text embedding."""
        tokens = clip_tokenize(prompt).to(self.device)
        embed = self.model.encode_text(tokens).float()
        return norm1(embed)

    def embed_cutout(self, image) -> torch.Tensor:
        """Normalized clip image embedding."""
        image = self.normalize(image)
        embed = self.model.encode_image(image)
        return norm1(embed)
