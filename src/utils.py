from math import ceil

import numpy as np
from PIL import Image


BLACK = np.array([0, 0, 0], np.uint8)
RED = np.array([200, 0, 0], np.uint8)
BLUE = np.array([100, 0, 250], np.uint8)
GREEN = np.array([0, 200, 0], np.uint8)
GRAY = np.array([127, 127, 127], np.uint8)

def toImage(array, name="default.bmp"):
    if not name.endswith(".bmp"):
        name += ".bmp"
    if len(array.shape) == 2:
        img = Image.fromarray(array, 'L')
    else:
        img = Image.fromarray(array, 'RGB')
    img.save('resources/' + name)

def resize(array, min_w = 2, min_h = 2):
    assert min_w % 2 == 0, f"Minimum width {min_w} must be even."
    assert min_h % 2 == 0, f"Minimum height {min_h} must be even."
    h = array.shape[0]
    w = array.shape[1]
    new_w = max(min_w, w)
    new_h = max(min_h, h)
    res = np.full((new_h, new_w, *array.shape[2:]), 255, dtype=array.dtype)
    y = (new_h - h) // 2
    x = (new_w - w) // 2
    res[y:y + h, x:x + w] = array
    return res

def drawHLine(array, x_min, x_max, y, color):
    h, w, _ = array.shape
    y = int(h / 2 - y)
    x_min = int(x_min + w / 2)
    x_max = ceil(x_max + w / 2)
    array[y, x_min:x_max] = color

def drawVLine(array, y_min, y_max, x, color):
    h, w, _ = array.shape
    y_max2 = int(h / 2 - y_min)
    y_min2 = ceil(h / 2 - y_max)
    x = int(x + w / 2)
    array[y_min2:y_max2, x] = color