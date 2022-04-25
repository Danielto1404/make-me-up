import os
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.utils.data as torch_data_utils
from PIL import Image


class MakeupDataset(torch_data_utils.Dataset):
    def __init__(self, root: str = 'images'):
        self.root = root
        self.semantic_dim = 18

        current_dir = Path('.') / 'static'

        self.makeup_path = [
            os.path.join(current_dir, self.root, 'makeup', name)
            for name in os.listdir(os.path.join(current_dir, self.root, 'makeup'))
        ]

        self.non_makeup_path = [
            os.path.join(current_dir, self.root, 'non-makeup', name)
            for name in os.listdir(os.path.join(current_dir, self.root, 'non-makeup'))
        ]

    @staticmethod
    def BGR2RGB(image):
        return cv2.cvtColor(image[:, :, :], cv2.COLOR_BGR2RGB)

    @staticmethod
    def rotate(img: np.ndarray, angle: float) -> np.ndarray:
        img = Image.fromarray(img)
        img = img.rotate(angle)
        img = np.array(img)
        return img

    def load_img(self, img_path: str, angle: float = 0):
        print(img_path)
        img = cv2.imread(img_path)
        img = self.BGR2RGB(img)
        img = self.rotate(img, angle)
        return img

    def load_parse(self, parse: str, angle: float = 0):
        parse = cv2.imread(parse, cv2.IMREAD_GRAYSCALE)
        parse = self.rotate(parse, angle)
        h, w = parse.shape
        result = np.zeros([h, w, self.semantic_dim])
        for i in range(self.semantic_dim):
            result[:, :, i][np.where(parse == i)] = 1
        result = np.array(result)
        return result

    @staticmethod
    def test_preprocessing(
            non_makeup_img,
            makeup_img,
            non_makeup_parse,
            makeup_parse,
            resize_size=512,
            crop_size=512
    ):
        non_makeup_img = cv2.resize(non_makeup_img, (resize_size, resize_size))
        makeup_img = cv2.resize(makeup_img, (resize_size, resize_size))
        non_makeup_parse = cv2.resize(non_makeup_parse, (resize_size, resize_size), interpolation=cv2.INTER_NEAREST)
        makeup_parse = cv2.resize(makeup_parse, (resize_size, resize_size), interpolation=cv2.INTER_NEAREST)

        h1 = int((resize_size - crop_size) / 2)
        w1 = int((resize_size - crop_size) / 2)

        non_makeup_img = non_makeup_img[h1:h1 + crop_size, w1:w1 + crop_size]
        non_makeup_parse = non_makeup_parse[h1:h1 + crop_size, w1:w1 + crop_size]
        makeup_img = makeup_img[h1:h1 + crop_size, w1:w1 + crop_size]
        makeup_parse = makeup_parse[h1:h1 + crop_size, w1:w1 + crop_size]

        non_makeup_img = non_makeup_img / 127.5 - 1.
        makeup_img = makeup_img / 127.5 - 1.

        preprocessed_data = {
            'non_makeup': non_makeup_img,
            'makeup': makeup_img,
            'non_makeup_parse': non_makeup_parse,
            'makeup_parse': makeup_parse
        }
        return preprocessed_data

    def __getitem__(self, index):
        non_makeup_index = index // len(self.makeup_path)
        makeup_index = index % len(self.makeup_path)

        non_makeup_img = self.load_img(self.non_makeup_path[non_makeup_index])
        non_makeup_parse = self.load_parse(self.non_makeup_path[non_makeup_index].replace('images', 'seg'))

        makeup_img = self.load_img(self.makeup_path[makeup_index])
        makeup_parse = self.load_parse(self.makeup_path[makeup_index].replace('images', 'seg'))

        data = self.test_preprocessing(non_makeup_img, makeup_img, non_makeup_parse, makeup_parse)
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

    def __len__(self):
        return len(self.makeup_path) * len(self.non_makeup_path)
