import pickle

import torch
import torch.nn.functional as F
import torchvision.transforms
from einops import rearrange


def load_gan(pickle_path, device='cpu'):
    """
    :param pickle_path: path to torch stylegan model
    :param device: torch device
    :return: Generator
    """
    with open(pickle_path, 'rb') as fp:
        state = pickle.load(fp)
        generator = state['G_ema']
        return generator.to(device)


def generate_image(G, latent=None, class_label=None, device='cpu'):
    if latent is None:
        latent = torch.randn([1, G.z_dim]).to(device)

    img = G(latent, class_label)
    return img


def norm1(prompt) -> torch.Tensor:
    """Normalize to the unit sphere."""
    return prompt / prompt.square().sum(dim=-1, keepdim=True).sqrt()


def spherical_dist_loss(x, y):
    x = F.normalize(x, dim=-1)
    y = F.normalize(y, dim=-1)
    return (x - y).norm(dim=-1).div(2).arcsin().pow(2).mul(2)


def prompts_dist_loss(x, targets, loss):
    # Keeps consistent results vs previous method for single objective guidance
    if len(targets) == 1:
        return loss(x, targets[0])
    distances = [loss(x, target) for target in targets]
    return torch.stack(distances, dim=-1).sum(dim=-1)


class MakeCutouts(torch.nn.Module):
    def __init__(self, cut_size, cutn, cut_pow=1.):
        super().__init__()
        self.cut_size = cut_size
        self.cutn = cutn
        self.cut_pow = cut_pow

    def forward(self, input):
        sideY, sideX = input.shape[2:4]
        max_size = min(sideX, sideY)
        min_size = min(sideX, sideY, self.cut_size)
        cutouts = []
        for _ in range(self.cutn):
            size = int(torch.rand([]) ** self.cut_pow * (max_size - min_size) + min_size)
            offset_x = torch.randint(0, sideX - size + 1, ())
            offset_y = torch.randint(0, sideY - size + 1, ())
            cutout = input[:, :, offset_y:offset_y + size, offset_x:offset_x + size]
            cutouts.append(F.adaptive_avg_pool2d(cutout, self.cut_size))
        return torch.cat(cutouts)


def embed_image(cutouts, clip, image):
    n = image.shape[0]
    cutouts = cutouts(image)
    embeds = clip.embed_cutout(cutouts)
    embeds = rearrange(embeds, '(cc n) c -> cc n c', n=n)
    return embeds


imagenet_normalize = torchvision.transforms.Normalize(
    mean=[0.48145466, 0.4578275, 0.40821073],
    std=[0.26862954, 0.26130258, 0.27577711]
)
