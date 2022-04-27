import numpy as np
import torch

from src.image_utils import resize_with_aspect


class MakeupTransferData:
    def __init__(
            self,
            source: np.ndarray,
            target: np.ndarray,
            source_parsing: np.ndarray,
            target_parsing: np.ndarray,
    ):
        self.source = source
        self.target = target
        self.source_parsing = source_parsing
        self.target_parsing = target_parsing
        self.semantic_dim = 18

    def preprocess_parsing(self, parsing: np.ndarray):
        h, w = parsing.shape

        result = np.zeros([h, w, self.semantic_dim])

        for i in range(self.semantic_dim):
            result[:, :, i][np.where(parsing == i)] = 1

        return result

    @staticmethod
    def preprocessing(
            non_makeup_img: np.ndarray,
            makeup_img: np.ndarray,
            non_makeup_parse: np.ndarray,
            makeup_parse: np.ndarray,
            resize_size=300,
            crop_size=256
    ):
        non_makeup_img = resize_with_aspect(non_makeup_img, resize_size)
        non_makeup_parse = resize_with_aspect(non_makeup_parse, resize_size)

        makeup_parse = resize_with_aspect(makeup_parse, resize_size)
        makeup_img = resize_with_aspect(makeup_img, resize_size)

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

    def get(self):
        non_makeup_img = self.source
        non_makeup_parse = self.preprocess_parsing(self.source_parsing)

        makeup_img = self.target
        makeup_parse = self.preprocess_parsing(self.target_parsing)

        data = self.preprocessing(non_makeup_img, makeup_img, non_makeup_parse, makeup_parse)
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
            'non_makeup': torch.from_numpy(non_makeup_img).unsqueeze(0).type(torch.FloatTensor),
            'makeup': torch.from_numpy(makeup_img).unsqueeze(0).type(torch.FloatTensor),
            'non_makeup_parse': torch.from_numpy(non_makeup_parse).unsqueeze(0).type(torch.FloatTensor),
            'makeup_parse': torch.from_numpy(makeup_parse).unsqueeze(0).type(torch.FloatTensor)
        }
        return data
