import pickle
from typing import Optional

import torch
import torch.nn as nn
from PIL import Image


class StyleganGenerator(nn.Module):
    def __init__(self, model_path: str, device: str):
        super().__init__()
        self.device = device
        self.generator = StyleganGenerator.load_weights(model_path, device)

    @staticmethod
    def load_weights(path: str, device: str):
        """
        Loads generator weight from `.pkl` file
        """
        with open(path, 'rb') as fp:
            state = pickle.load(fp)
            generator = state['G_ema'].to(device)

        return generator

    def mapping(
            self,
            latent: torch.Tensor,
            class_label: Optional[int] = None,
            truncation_psi: float = 0.8
    ) -> torch.Tensor:
        return self.generator.mapping(latent, class_label, truncation_psi=truncation_psi)

    def synthesis(self, latent: torch.Tensor, noise_mode: Optional[str] = None) -> torch.Tensor:
        """
        Returns generated image with given latent vector
        """
        return self.generator.synthesis(latent, noise_mode)

    @property
    def w_avg(self) -> torch.Tensor:
        """
        Returns average weights of `mapping` network
        """
        return self.generator.mapping.w_avg

    @property
    def z_dim(self) -> torch.Tensor:
        """
        Returns dimension of latent vector
        """
        return self.generator.mapping.z_dim

    def gen_image(self) -> Image:
        print('generating random image...')
        latent = 2 * torch.randn([1, self.z_dim]).to(self.device)
        label = None
        image = self.generator(latent, label, truncation_psi=1, noise_mode='const')
        image = (image.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8).cpu().numpy()[0]
        return Image.fromarray(image, 'RGB')
