import pickle
import sys
import torch

from src.models import CLIPTrainer, CLIP
from utils import read_config

sys.path.append("./models")

config = read_config()
device = config["models"]["device"]
wstds = torch.load(config["models"]["wstds"]).to(device)

try:
    with open(config["models"]["stylegan"], "rb") as fp:
        G = pickle.load(fp)["G_ema"].to(device)

except Exception as e:
    raise "Can't loading gan model"

clip = CLIP(model_name=config["models"]["clip"], device=device)

trainer = CLIPTrainer(G=G, clip_model=clip, w_stds=wstds, device=device)
