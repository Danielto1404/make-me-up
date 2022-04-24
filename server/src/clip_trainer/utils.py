import torch
import torch.nn.functional as F
from einops import rearrange


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
