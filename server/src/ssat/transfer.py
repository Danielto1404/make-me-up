from pathlib import Path

import torch
import torch.utils.data as torch_data

from .dataset import MakeupDataset
from .model import MakeupGAN


def transfer(ssat_model: MakeupGAN, root: str = 'images'):
    print(Path('.').resolve())
    dataset = MakeupDataset(root)
    train_loader = torch_data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)

    for data in train_loader:
        with torch.no_grad():
            return ssat_model.test_pair(data)
