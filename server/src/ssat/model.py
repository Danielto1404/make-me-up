import torch
import torch.nn as nn

from .make_options import MakeOptions
from .networks import init_net, E_makeup, E_content, E_semantic, Transformer, Decoder


class MakeupGAN(nn.Module):
    def __init__(self, device, opts=MakeOptions()):
        super(MakeupGAN, self).__init__()
        self.opts = opts

        # parameters
        self.lr = opts.lr
        self.batch_size = opts.batch_size

        self.device = torch.device(device)
        self.input_dim = opts.input_dim
        self.output_dim = opts.output_dim
        self.semantic_dim = opts.semantic_dim

        # encoders
        self.enc_content = init_net(E_content(opts.input_dim), self.device, init_type='normal', gain=0.02)
        self.enc_makeup = init_net(E_makeup(opts.input_dim), self.device, init_type='normal', gain=0.02)
        self.enc_semantic = init_net(E_semantic(opts.semantic_dim), self.device, init_type='normal', gain=0.02)
        self.transformer = init_net(Transformer(), self.device, init_type='normal', gain=0.02)
        # generator
        self.gen = init_net(Decoder(opts.output_dim), self.device, init_type='normal', gain=0.02)

    def forward(self):
        # first clip_trainer and removal
        self.z_non_makeup_c = self.enc_content(self.non_makeup)
        self.z_non_makeup_s = self.enc_semantic(self.non_makeup_parse)
        self.z_non_makeup_a = self.enc_makeup(self.non_makeup)

        self.z_makeup_c = self.enc_content(self.makeup)
        self.z_makeup_s = self.enc_semantic(self.makeup_parse)
        self.z_makeup_a = self.enc_makeup(self.makeup)
        # warp makeup style
        self.mapX, self.mapY, self.z_non_makeup_a_warp, self.z_makeup_a_warp = self.transformer(
            self.z_non_makeup_c,
            self.z_makeup_c,
            self.z_non_makeup_s,
            self.z_makeup_s,
            self.z_non_makeup_a,
            self.z_makeup_a
        )
        # makeup clip_trainer and removal
        self.z_transfer = self.gen(self.z_non_makeup_c, self.z_makeup_a_warp)
        self.z_removal = self.gen(self.z_makeup_c, self.z_non_makeup_a_warp)

        # rec
        self.z_rec_non_makeup = self.gen(self.z_non_makeup_c, self.z_non_makeup_a)
        self.z_rec_makeup = self.gen(self.z_makeup_c, self.z_makeup_a)

        # second clip_trainer and removal
        self.z_transfer_c = self.enc_content(self.z_transfer)
        # self.z_non_makeup_s = self.enc_semantic(self.non_makeup_parse)
        self.z_transfer_a = self.enc_makeup(self.z_transfer)

        self.z_removal_c = self.enc_content(self.z_removal)
        # self.z_makeup_s = self.enc_semantic(self.makeup_parse)
        self.z_removal_a = self.enc_makeup(self.z_removal)
        # warp makeup style
        self.mapX2, self.mapY2, self.z_transfer_a_warp, self.z_removal_a_warp = self.transformer(
            self.z_transfer_c,
            self.z_removal_c,
            self.z_non_makeup_s,
            self.z_makeup_s,
            self.z_transfer_a,
            self.z_removal_a
        )
        # makeup clip_trainer and removal
        self.z_cycle_non_makeup = self.gen(self.z_transfer_c, self.z_removal_a_warp)
        self.z_cycle_makeup = self.gen(self.z_removal_c, self.z_transfer_a_warp)

    def resume(self, model_dir, train=True):
        if self.device.type == 'cpu':
            checkpoint = torch.load(model_dir, map_location='cpu')
        else:
            checkpoint = torch.load(model_dir)

        # weight
        self.enc_content.load_state_dict(checkpoint['enc_c'])
        self.enc_makeup.load_state_dict(checkpoint['enc_a'])
        self.enc_semantic.load_state_dict(checkpoint['enc_s'])
        self.transformer.load_state_dict(checkpoint['enc_trans'])
        self.gen.load_state_dict(checkpoint['gen'])
        return checkpoint['ep'], checkpoint['total_it']

    @staticmethod
    def normalize_image(x):
        return x[:, 0:3, :, :]

    @torch.no_grad()
    def test_pair(self, data) -> torch.Tensor:
        self.non_makeup = data['non_makeup'].to(self.device).detach()
        self.makeup = data['makeup'].to(self.device).detach()
        self.non_makeup_parse = data['non_makeup_parse'].to(self.device).detach()
        self.makeup_parse = data['makeup_parse'].to(self.device).detach()

        self.z_non_makeup_c = self.enc_content(self.non_makeup)
        self.z_non_makeup_s = self.enc_semantic(self.non_makeup_parse)
        self.z_non_makeup_a = self.enc_makeup(self.non_makeup)

        self.z_makeup_c = self.enc_content(self.makeup)
        self.z_makeup_s = self.enc_semantic(self.makeup_parse)
        self.z_makeup_a = self.enc_makeup(self.makeup)

        # warp makeup style
        self.mapX, self.mapY, self.z_non_makeup_a_warp, self.z_makeup_a_warp = self.transformer(
            self.z_non_makeup_c,
            self.z_makeup_c,
            self.z_non_makeup_s,
            self.z_makeup_s,
            self.z_non_makeup_a,
            self.z_makeup_a
        )
        # makeup clip_trainer and removal
        self.z_transfer = self.gen(self.z_non_makeup_c, self.z_makeup_a_warp)
        self.z_removal = self.gen(self.z_makeup_c, self.z_non_makeup_a_warp)

        images_z_transfer = self.normalize_image(self.z_transfer).detach()

        return images_z_transfer[0:1, ::]
