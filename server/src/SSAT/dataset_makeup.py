import os

import cv2
import numpy as np
import torch
import torch.utils.data as data
from PIL import Image


class MakeupDataset(data.Dataset):
    def __init__(self, opts):
        self.opt = opts
        self.data_root = opts.dataroot
        self.semantic_dim = opts.semantic_dim

        # non_makeup
        print(os.path.join(self.data_root, 'non-makeup'))
        name_non_makeup = os.listdir(os.path.join(self.data_root, 'non-makeup'))
        name_non_makeup = list(filter(lambda name: name[0] != '.', name_non_makeup))
        self.non_makeup_path = [os.path.join(self.data_root, 'non-makeup', x) for x in name_non_makeup]

        # makeup
        name_makeup = os.listdir(os.path.join(self.data_root, 'makeup'))
        name_makeup = list(filter(lambda name: name[0] != '.', name_makeup))
        self.makeup_path = [os.path.join(self.data_root, 'makeup', x) for x in name_makeup]

        self.warp_root = os.path.join(self.data_root, 'warp')

        self.non_makeup_size = len(self.non_makeup_path)
        self.makeup_size = len(self.makeup_path)

        if self.opt.phase == 'train':
            self.dataset_size = self.non_makeup_size
        else:
            # self.dataset_size = self.non_makeup_size
            self.dataset_size = self.non_makeup_size * self.makeup_size

    @staticmethod
    def BGR2RGB(image):
        return cv2.cvtColor(image[:, :, :], cv2.COLOR_BGR2RGB)

    def load_img(self, img_path, angle=0):
        print(img_path)
        img = cv2.imread(img_path)
        img = self.BGR2RGB(img)
        img = self.rotate(img, angle)
        return img

    def load_parse(self, parse, angle=0):
        parse = cv2.imread(parse, cv2.IMREAD_GRAYSCALE)
        parse = self.rotate(parse, angle)
        h, w = parse.shape
        result = np.zeros([h, w, self.semantic_dim])
        for i in range(self.semantic_dim):
            result[:, :, i][np.where(parse == i)] = 1
        result = np.array(result)
        return result

    @staticmethod
    def rotate(img, angle):
        img = Image.fromarray(img)
        img = img.rotate(angle)
        img = np.array(img)
        return img

    def __getitem__(self, index):
        if self.opt.phase == 'test_pair':
            non_makeup_index = index // self.makeup_size
            makeup_index = index % self.makeup_size

            non_makeup_angle = 0
            makeup_angle = 0

            non_makeup_img = self.load_img(self.non_makeup_path[non_makeup_index], non_makeup_angle)
            non_makeup_parse = self.load_parse(self.non_makeup_path[non_makeup_index].replace('images', 'seg1'),
                                               non_makeup_angle)

            makeup_img = self.load_img(self.makeup_path[makeup_index], makeup_angle)
            makeup_parse = self.load_parse(self.makeup_path[makeup_index].replace('images', 'seg1'), makeup_angle)

            data = self.test_preprocessing(self.opt, non_makeup_img, makeup_img, non_makeup_parse, makeup_parse)
            non_makeup_img = data['non_makeup']
            makeup_img = data['makeup']
            non_makeup_parse = data['non_makeup_parse']
            makeup_parse = data['makeup_parse']

            non_makeup_img = np.transpose(non_makeup_img, (2, 0, 1))
            makeup_img = np.transpose(makeup_img, (2, 0, 1))
            non_makeup_parse = np.transpose(non_makeup_parse, (2, 0, 1))
            makeup_parse = np.transpose(makeup_parse, (2, 0, 1))
            non_makeup_parse = np.clip(non_makeup_parse, a_min=0, a_max=1)
            makeup_parse = np.clip(makeup_parse, a_min=0, a_max=1)

            data = {
                'non_makeup': torch.from_numpy(non_makeup_img).type(torch.FloatTensor),
                'makeup': torch.from_numpy(makeup_img).type(torch.FloatTensor),
                'non_makeup_parse': torch.from_numpy(non_makeup_parse).type(torch.FloatTensor),
                'makeup_parse': torch.from_numpy(makeup_parse).type(torch.FloatTensor)
            }
            return data

    @staticmethod
    def test_preprocessing(opts, non_makeup_img, makeup_img, non_makeup_parse, makeup_parse):
        non_makeup_img = cv2.resize(non_makeup_img, (opts.resize_size, opts.resize_size))
        makeup_img = cv2.resize(makeup_img, (opts.resize_size, opts.resize_size))
        non_makeup_parse = cv2.resize(non_makeup_parse, (opts.resize_size, opts.resize_size),
                                      interpolation=cv2.INTER_NEAREST)
        makeup_parse = cv2.resize(makeup_parse, (opts.resize_size, opts.resize_size),
                                  interpolation=cv2.INTER_NEAREST)
        h1 = int((opts.resize_size - opts.crop_size) / 2)
        w1 = int((opts.resize_size - opts.crop_size) / 2)
        non_makeup_img = non_makeup_img[h1:h1 + opts.crop_size, w1:w1 + opts.crop_size]
        non_makeup_parse = non_makeup_parse[h1:h1 + opts.crop_size, w1:w1 + opts.crop_size]
        makeup_img = makeup_img[h1:h1 + opts.crop_size, w1:w1 + opts.crop_size]
        makeup_parse = makeup_parse[h1:h1 + opts.crop_size, w1:w1 + opts.crop_size]

        non_makeup_img = non_makeup_img / 127.5 - 1.
        makeup_img = makeup_img / 127.5 - 1.

        preprocessed_data = {
            'non_makeup': non_makeup_img,
            'makeup': makeup_img,
            'non_makeup_parse': non_makeup_parse,
            'makeup_parse': makeup_parse
        }
        return preprocessed_data

    def __len__(self):
        return self.dataset_size

    @staticmethod
    def expand_mask(mask):
        mask = np.expand_dims(mask, axis=2)
        mask = np.concatenate((mask, mask, mask), axis=2)
        return mask
