import pickle
import sys
from pathlib import Path

import yaml

root_path = Path('..')

sys.path.append("./src/models")


def read_config():
    with open('config.yaml') as stream:
        return yaml.safe_load(stream)


def load_gan_generator(path, device):
    # loguru.Level("Loading generator")
    with open(path, 'rb') as fp:
        G = pickle.load(fp)['G_ema'].to(device)

    return G
