from .make_options import MakeOptions
from .model import MakeupGAN


def load_ssat_model(path, device='cpu'):
    opts = MakeOptions(device=device)
    model = MakeupGAN(opts)

    _ = model.resume(path, train=False)

    return model
