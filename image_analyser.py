from PIL import Image
import numpy as np


def load_image_to_array(fname, res=None):
    """
    fname: string, name of jpg
    res: (int, int), resolution to resize/reduce to
    return: numpy.array, pixel RGB

    """
    img = Image.open(fname)
    if res:
        img = img.resize(res)
    return np.array(img)


def subtract_images(img1, img2):
    """
    img1, img2: numpy array 3d, input images
    return: numpy array, 1d n_pixel sum over RGB channels
    """
    diff = img1.astype(float) - img2.astype(float)
    abs_diff = np.abs(diff)
    sum_diff = abs_diff.sum(axis=-1)
    return sum_diff.flatten()


def detect_by_subtraction(img1, img2, diff_thres=100, frac_thres=0.1):
    """
    img1, img2: numpy array 3d, input images
    return: bool, movement detected
    """
    diff = subtract_images(img1, img2)
    diff_frac = np.mean(diff > diff_thres)
    return diff_frac > frac_thres
