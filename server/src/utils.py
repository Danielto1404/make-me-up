import torch
import torchvision

imagenet_normalize = torchvision.transforms.Normalize(
    mean=[0.48145466, 0.4578275, 0.40821073],
    std=[0.26862954, 0.26130258, 0.27577711]
)


def norm1(prompt: torch.Tensor) -> torch.Tensor:
    """Normalize to the unit sphere."""
    return prompt / prompt.square().sum(dim=-1, keepdim=True).sqrt()
