from random import randint
from typing import List

import torch
import torchvision.transforms.functional as TransformsFunctional
from PIL import Image
from tqdm import tqdm

from .losses import prompts_dist_loss, spherical_dist_loss
from .utils import embed_image, MakeCutouts
from ..clip import CLIP
from ..stylegan import StyleganGenerator


class CLIPTrainer:
    def __init__(
            self,
            generator: StyleganGenerator,
            clip_model: CLIP,
            w_stds: torch.Tensor,
            device: str
    ):
        self.generator = generator
        self.clip_model = clip_model
        self.device = device
        self.cutouts = MakeCutouts(224, 32, 0.5).to(device)
        self.w_stds = w_stds

    def _initial_search(
            self,
            targets,
            iterations=50,
            batch_size=4,
            truncation_psi=1.0,
            seed=239
    ):
        torch.manual_seed(seed)

        qs = []
        losses = []

        for _ in tqdm(range(iterations), desc="Sampling initial vector"):
            latent = torch.randn([batch_size, self.generator.z_dim]).to(self.device)
            latent = self.generator.mapping(latent, truncation_psi=truncation_psi)
            latent = (latent - self.generator.w_avg) / self.w_stds

            images = self.generator.synthesis(latent)
            embeds = embed_image(
                cutouts=self.cutouts,
                clip=self.clip_model,
                image=images.add(1).div(2)
            )

            loss = prompts_dist_loss(embeds, targets, spherical_dist_loss).mean(0)
            i = torch.argmin(loss)

            qs.append(latent[i])
            losses.append(loss[i])

        qs = torch.stack(qs)
        losses = torch.stack(losses)
        i = torch.argmin(losses)
        latent = qs[i].unsqueeze(0).requires_grad_()

        return latent

    def _optimize(self, initial, targets, iterations):

        assert iterations > 0, "Amount of iteration must be >= 1"

        pil_image = None

        q = initial
        q_ema = q

        optimizer = torch.optim.AdamW([q], lr=0.05, betas=(0.1, 0.99))
        loop = tqdm(range(iterations), desc='Optimizing latent vector')

        for _ in loop:
            optimizer.zero_grad()
            w = q * self.w_stds

            image = self.generator.synthesis(w + self.generator.w_avg, noise_mode='const')

            embed = embed_image(
                cutouts=self.cutouts,
                clip=self.clip_model,
                image=image.add(1).div(2)
            )

            loss = prompts_dist_loss(embed, targets, spherical_dist_loss).mean()

            loss.backward()
            optimizer.step()

            loop.set_postfix(loss=loss.item(), q_magnitude=q.std().item())

            q_ema = q_ema * 0.95 + q * 0.05

            image = self.generator.synthesis(q_ema * self.w_stds + self.generator.w_avg, noise_mode='const')
            pil_image = TransformsFunctional.to_pil_image(image[0].add(1).div(2).clamp(0, 1))

        return pil_image

    def train(
            self,
            prompts: List[str],
            initial_iterations: int = 1,
            iterations: int = 1,
            batch_size: int = 1,
            truncation_psi: float = 0.75
    ) -> Image:
        targets = [self.clip_model.embed_text(text) for text in prompts]

        initial = self._initial_search(
            targets,
            iterations=initial_iterations,
            batch_size=batch_size,
            truncation_psi=truncation_psi,
            seed=randint(0, 1_000_000)
        )

        torch.cuda.empty_cache()

        image = self._optimize(initial, targets, iterations=iterations)
        torch.cuda.empty_cache()

        return image
