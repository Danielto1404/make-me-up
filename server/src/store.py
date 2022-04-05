import pickle
import sys

from src.models import CLIPTrainer, CLIP
from utils import read_config

sys.path.append("./models")

config = read_config()
device = config["models"]["device"]

try:
    with open(config["models"]["stylegan"], "rb") as fp:
        G = pickle.load(fp)["G_ema"].to(device)

except Exception as e:
    raise "Can't loading gan model"

clip = CLIP(model_name=config["models"]["clip"], device=device)

trainer = CLIPTrainer(G=G, clip_model=clip, device=device)
