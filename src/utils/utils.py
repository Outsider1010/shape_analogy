from typing import Any

from numpy import uint8, where, array as c_array, zeros, ndarray, dtype
from PIL import Image
from math import ceil

from src.utils.constants import LEFT_RIGHT, UP_DOWN

def find_unique_bool(bool_list: tuple[bool, ...]):
    count_true = count_false = elem_true = elem_false = 0
    for i in range(len(bool_list)):
        if bool_list[i]:
            count_true += 1
            elem_true = i
        else:
            count_false += 1
            elem_false = i
    if count_true == 1:
        return elem_true
    if count_false == 1:
        return elem_false
    return None


def aux(__corner: int):
    return (__corner & LEFT_RIGHT) - 1, ((__corner & UP_DOWN) // 4) - 1


# Black -> True
# Anything else -> False
def image_to_array(img) -> ndarray[bool, dtype[bool]]:
    return where(c_array(Image.open(img)) == 0, True, False)


def array_to_image(array, name="default.bmp"):
    img = Image.fromarray(uint8(where(array, 0, 255)), 'L')
    img.save('resources/'+name)


def arr_range(arr, x_min, x_max, y_min, y_max):
    w, h = arr.shape
    b1 = int(y_min + w / 2)
    b2 = b1 + round(y_max - y_min)
    b3 = int(x_min + h / 2)
    b4 = b3 + round(x_max - x_min)
    return arr[b1:b2, b3:b4]


def arr_set_range_value(arr, x_min, x_max, y_min, y_max, value):
    w, h = arr.shape
    b1 = int(y_min + w / 2)
    b2 = b1 + round(y_max - y_min)
    b3 = int(x_min + h / 2)
    b4 = b3 + round(x_max - x_min)
    arr[b1:b2, b3:b4] |= value
