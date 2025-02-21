import numpy as np
from PIL import Image


def toImage(array, name="default.bmp"):
    if not name.endswith(".bmp"):
        name += ".bmp"
    img = Image.fromarray(array, 'L')
    img.save('resources/' + name)

def resize2D(array, min_w = 2, min_h = 2):
    assert min_w % 2 == 0, f"Minimum width {min_w} must be even."
    assert min_h % 2 == 0, f"Minimum height {min_h} must be even."
    h, w = array.shape
    new_w = max(min_w, w)
    new_h = max(min_h, h)
    res = np.ones((new_h, new_w), dtype=array.dtype) * 255
    y = (new_h - h) // 2
    x = (new_w - w) // 2
    res[y:y + h, x:x + w] = array
    return res