import os
import warnings

import torch
import torch.utils.data as torch_data
import torchvision.utils

from .dataset_makeup import MakeupDataset
from .make_options import MakeOptions
from .model import MakeupGAN
from .options import MakeupOptions
from .saver import Saver

warnings.filterwarnings("ignore")
os.environ['CUDA_VISIBLE_DEVICES'] = '0'


def pair_test():
    # parse options
    parser = MakeupOptions()
    opts = parser.parse()
    opts.phase = 'test_pair'
    # data loader
    print('\n--- load dataset ---')
    dataset = MakeupDataset(opts)
    train_loader = torch_data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)
    print(len(train_loader))

    # model
    print('\n--- load model ---')
    model = MakeupGAN(opts)

    _ = model.resume(os.path.join('../../static', 'SSAT.pth'), train=False)
    model.eval()
    print('start pair test')
    # saver for display and output
    saver = Saver(opts)
    for iteration, data in enumerate(train_loader):
        with torch.no_grad():
            saver.write_test_pair_img(iteration, model, data)


def transfer(ssat_model, options: MakeOptions):
    options.phase = 'test_pair'
    dataset = MakeupDataset(options)
    train_loader = torch_data.DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)

    for data in train_loader:
        with torch.no_grad():
            root = os.path.join(options.result_dir, 'test_pair')
            if not os.path.exists(root):
                os.makedirs(root)
            test_pair, make_image = ssat_model.test_pair(data)
            torchvision.utils.save_image(make_image / 2 + 0.5, f"{root}/result.jpg", nrow=1)
