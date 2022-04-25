import pickle
from typing import Optional

import torch

from config import read_config
from src.clip import CLIP
from src.clip_trainer.train import CLIPTrainer
from src.faceparsing import FaceParser
from src.ssat import MakeupGAN

_face_parser: Optional[FaceParser] = None
_clip_model: Optional[CLIP] = None
_gan_model = None
_ssat_model: Optional[MakeupGAN] = None
_clip_trainer: Optional[CLIPTrainer] = None

_config = read_config()


def get_face_parser() -> FaceParser:
    global _face_parser

    if _face_parser is None:
        _face_parser = FaceParser(
            model_path=_config['models']['faceparsing'],
            device=_config['models']['device']
        )

    return _face_parser


def get_clip_model() -> CLIP:
    global _clip_model

    if _clip_model is None:
        _clip_model = CLIP(
            model_name=_config['models']['clip'],
            device=_config['models']['device']
        )

    return _clip_model


def get_gan_model() -> torch.nn:
    global _gan_model

    if _gan_model is None:
        with open(_config['models']['stylegan'], 'rb') as fp:
            state = pickle.load(fp)
            _gan_model = state['G_ema'].to(_config['models']['device'])

    return _gan_model


def get_ssat_model() -> MakeupGAN:
    global _ssat_model

    if _ssat_model is None:
        _ssat_model = MakeupGAN(device=_config['models']['device'])
        _ssat_model.resume(_config['models']['ssat'], train=False)
        _ssat_model.eval()

    return _ssat_model


def get_clip_trainer() -> CLIPTrainer:
    global _clip_trainer

    if _clip_trainer is None:
        _clip_trainer = CLIPTrainer(
            G=get_gan_model(),
            clip_model=get_clip_model(),
            w_stds=torch.load(_config['models']['wstds']),
            device=_config['models']['device']
        )

    return _clip_trainer
