import os
from typing import Tuple, List

import torch
import torchvision.transforms.functional as TF
from tqdm import tqdm

from .utils import embed_image, prompts_dist_loss, spherical_dist_loss, MakeCutouts
from ..clip import CLIP


class CLIPTrainer:
    def __init__(self, G: any, clip_model: CLIP, w_stds: torch.Tensor, device: str):
        self.G = G
        self.clip_model = clip_model
        self.device = device
        self.cutouts = MakeCutouts(224, 32, 0.5)
        self.w_stds = w_stds

    @staticmethod
    def _find_weights_std(G: any, device) -> Tuple[torch.nn.Module, torch.Tensor]:
        """
        Loads stylegan generator, and find's std weights vector.
        :return: Std weights
        """
        print(f'Finding std weights')
        zs = torch.randn([5000, G.mapping.z_dim], device=device)
        w_stds = G.mapping(zs, None).std(0)
        print(f'Found std weights')
        return w_stds

    def _initial_search(
            self,
            targets,
            iterations=50,
            batch_size=4,
            truncation_psi=1.0,
            seed=239
    ):
        torch.manual_seed(seed)

        G = self.G
        w_stds = self.w_stds
        cutouts = self.cutouts

        qs = []
        losses = []

        for _ in tqdm(range(iterations), desc="Sampling initial vector"):
            latent = torch.randn([batch_size, G.mapping.z_dim]).to(self.device)
            class_ = None
            latent = G.mapping(latent, class_, truncation_psi=truncation_psi)
            latent = (latent - G.mapping.w_avg) / w_stds

            images = G.synthesis(latent)
            embeds = embed_image(
                cutouts=cutouts,
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

        G = self.G
        w_stds = self.w_stds
        cutouts = self.cutouts

        q = initial
        q_ema = q

        optimizer = torch.optim.AdamW([q], lr=0.05, betas=(0.1, 0.99))
        loop = tqdm(range(iterations), desc='Optimizing latent vector')

        for i in loop:
            optimizer.zero_grad()
            w = q * self.w_stds

            image = G.synthesis(w + G.mapping.w_avg, noise_mode='const')

            embed = embed_image(
                cutouts=cutouts,
                clip=self.clip_model,
                image=image.add(1).div(2)
            )

            loss = prompts_dist_loss(embed, targets, spherical_dist_loss).mean()

            loss.backward()
            optimizer.step()

            loop.set_postfix(loss=loss.item(), q_magnitude=q.std().item())

            q_ema = q_ema * 0.9 + q * 0.1

            image = G.synthesis(q_ema * w_stds + G.mapping.w_avg, noise_mode='const')
            pil_image = TF.to_pil_image(image[0].add(1).div(2).clamp(0, 1))
            os.makedirs(f'samples/', exist_ok=True)
            pil_image.save(f'samples/{i}-latent.jpg')

            yield i

        return q_ema

    def train(
            self,
            prompts: List[str],
            initial_iterations: int = 1,
            iterations: int = 1,
            batch_size: int = 1,
            truncation_psi: float = 0.75
    ):
        targets = [self.clip_model.embed_text(text) for text in prompts]

        initial = self._initial_search(
            targets,
            iterations=initial_iterations,
            batch_size=batch_size,
            truncation_psi=truncation_psi
        )

        latent = self._optimize(initial, targets, iterations=iterations)

        return latent
