import numpy as np
import torch

from .dataset import MakeupTransferData
from .model import MakeupGAN


@torch.no_grad()
def transfer(
        ssat_model: MakeupGAN,
        source: np.ndarray,
        target: np.ndarray,
        source_parsing: np.ndarray,
        target_parsing: np.ndarray
) -> torch.Tensor:
    data = MakeupTransferData(source, target, source_parsing, target_parsing).get()
    return ssat_model.test_pair(data)
