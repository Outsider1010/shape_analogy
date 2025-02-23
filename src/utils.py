import numpy as np
from PIL import Image

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
    v = 255
    if array.dtype == bool:
        v = False
    res = np.full((new_h, new_w, *array.shape[2:]), v, dtype=array.dtype)
    y = (new_h - h) // 2
    x = (new_w - w) // 2
    res[y:y + h, x:x + w] = array
    return res