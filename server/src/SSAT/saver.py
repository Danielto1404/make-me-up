import os

import cv2
import numpy as np
import torchvision


def tensor2img(img):
    img = img.cpu()[0].float().numpy()
    if img.shape[0] == 1:
        img = np.tile(img, (3, 1, 1))
    img = (np.transpose(img, (1, 2, 0)) + 1) / 2.0 * 255.0
    return img.astype(np.uint8)


def save_images(images, names, path):
    if not os.path.exists(path):
        os.mkdir(path)
    for img, name in zip(images, names):
        img = tensor2img(img)
        img = np.array(img)
        cv2.imwrite(os.path.join(path, name + '.jpg'), img)


class Saver:
    def __init__(self, opts):
        self.result_dir = opts.result_dir
        # make directory
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    # save test pair images
    def write_test_pair_img(self, iter, model, data):
        root = os.path.join(self.result_dir, 'test_pair')
        if not os.path.exists(root):
            os.makedirs(root)
        test_pair_img, make_image = model.test_pair(data)
        img_filename = '%s/gen_%05d.jpg' % (root, iter)
        make_filename = '%s/gen_%05d-make.jpg' % (root, iter)
        torchvision.utils.save_image(test_pair_img / 2 + 0.5, img_filename, nrow=1)
        torchvision.utils.save_image(make_image / 2 + 0.5, make_filename, nrow=1)
