import numpy as np
from math import ceil
from numpy import unravel_index, rot90, zeros, argmax

from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.rectangle import Rectangle
from . shape import Shape
from ..point import Point
from ..utils import image_to_array, arr_set_range_value_from_array
# DO NOT IMPORT STRATEGIES

class PixelShape(Shape):

    def __init__(self, array):
        self.pixels = array

    @staticmethod
    def fromImage(img):
        return PixelShape(image_to_array(img))

    @staticmethod
    def fromRectangle(rectangle):
        r0 = rectangle
        w, h = ceil(max(2 * abs(r0.y_min), 2 * abs(r0.y_max))), ceil(max(2 * abs(r0.x_min), 2 * abs(r0.x_max)))
        array = zeros((w, h), dtype=bool)
        array[int(r0.y_min + w / 2):int(r0.y_max + w / 2), int(r0.x_min + h / 2):int(r0.x_max + h / 2)] = True

        # for r in rectangles[1:]:
        #     a_w, a_h = array.shape
        #     w, h = (ceil(max(2 * abs(r.y_min), 2 * abs(r.y_max), a_w)),
        #             ceil(max(2 * abs(r.x_min), 2 * abs(r.x_max), a_h)))
        #     if w != a_w or h != a_h:
        #         array = zeros((w, h), dtype=bool)
        #         array[int((w - a_w) / 2):int((w + a_w) / 2), int((h - a_h) / 2):int((h + a_h) / 2)] = array
        #     array[int(r.y_min + w / 2):int(r.y_max + w / 2), int(r.x_min + h / 2):int(r.x_max + h / 2)] = True

        return PixelShape(array=array)

    def fromShape(self, x_min, x_max, y_min, y_max):
        array = np.zeros((ceil(max(2 * abs(y_min), 2 * abs(y_max))),
                                ceil(max(2 * abs(x_min), 2 * abs(x_max)))), dtype=bool)
        arr_set_range_value_from_array(array, x_min, x_max, y_min, y_max, self.pixels)
        return PixelShape(array=array)

    def getOuterRectangle(self) -> Rectangle:
        w, h = self.pixels.shape
        ind = unravel_index(argmax(self.pixels), self.pixels.shape)[0]
        y_max = w / 2 - ind
        temp = rot90(self.pixels[ind:])
        ind = unravel_index(argmax(temp), temp.shape)[0]
        x_max = (h - ind) - h / 2
        temp = rot90(temp[ind:])
        ind = unravel_index(argmax(temp), temp.shape)[0]
        y_min = ind - w / 2
        temp = rot90(temp[ind:])
        x_min = unravel_index(argmax(temp), temp.shape)[0] - h / 2
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerFramePixels(self)

    def cut(self, birectangle: BiRectangle, strategy):
        return strategy.cutPixels(self, birectangle)

    def isPointInShape(self, p: Point) -> bool:
        return self.pixels[int(p.y + self.width() / 2)][int(p.x + self.height() / 2)]

    def __eq__(self, other):
        if not isinstance(other, PixelShape):
            return False
        w1, h1 = self.pixels.shape
        w2, h2 = other.pixels.shape
        w = max(w1, w2)
        h = max(h1, h2)
        new_self_pixels = np.zeros((w, h), dtype=bool)
        new_other_pixels = np.zeros((w, h), dtype=bool)
        arr_set_range_value_from_array(new_self_pixels, - h1/2, h1/2, -w1/2, w1/2, self.pixels)
        arr_set_range_value_from_array(new_other_pixels, -h2/2, h2/2, -w2/2, w2/2, other.pixels)
        return np.all(new_self_pixels == new_other_pixels)

    def width(self) -> float:
        return self.pixels.shape[0]

    def height(self) -> float:
        return self.pixels.shape[1]

    def isEmpty(self) -> bool:
        return not self.pixels.any()

    def dim(self) -> tuple[float, float]:
        return self.pixels.shape
