import torch
import torch.nn.functional as F


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
