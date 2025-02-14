import numpy as np
from math import ceil
from numpy import unravel_index, rot90, zeros, argmax

from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.rectangle import Rectangle
from . shape import Shape
from src.biframemethod.point import Point
from PIL import Image
# DO NOT IMPORT STRATEGIES

class PixelShape(Shape):

    def __init__(self, array=None, img=None, rect=None):
        assert(array or img or rect, "One of the parameters (array, img, rect) must be set")
        if img:
            array = np.where(np.array(Image.open(img)) == 0, True, False)

        if rect:
            w, h = (ceil(max(2 * abs(rect.y_min), 2 * abs(rect.y_max))),
                    ceil(max(2 * abs(rect.x_min), 2 * abs(rect.x_max))))
            array = zeros((w, h), dtype=bool)
            array[int(rect.y_min + w / 2):int(rect.y_max + w / 2), int(rect.x_min + h / 2):int(rect.x_max + h / 2)] = True

        self.pixels: np.ndarray[bool] = array


    def fromShape(self, x_min, x_max, y_min, y_max):
        array = np.zeros((ceil(max(2 * abs(y_min), 2 * abs(y_max))),
                                ceil(max(2 * abs(x_min), 2 * abs(x_max)))), dtype=bool)
        self.__set_values_from_this(array, x_min, x_max, y_min, y_max)
        return PixelShape(array=array)

    def __set_values_from_this(self, arr, x_min, x_max, y_min, y_max):
        w, h = arr.shape
        b1 = int(y_min + w / 2)
        b2 = b1 + round(y_max - y_min)
        b3 = int(x_min + h / 2)
        b4 = b3 + round(x_max - x_min)

        w, h = self.dim()
        c1 = int(y_min + w / 2)
        c2 = c1 + round(y_max - y_min)
        c3 = int(x_min + h / 2)
        c4 = c3 + round(x_max - x_min)
        arr[b1:b2, b3:b4] |= self.pixels[c1:c2, c3:c4]

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
        return self.pixels[int(p.y + self.width() / 2), int(p.x + self.height() / 2)]

    def __eq__(self, other):
        if not isinstance(other, PixelShape):
            return False
        w1, h1 = self.pixels.shape
        w2, h2 = other.pixels.shape
        w = max(w1, w2)
        h = max(h1, h2)
        new_self_pixels = np.zeros((w, h), dtype=bool)
        new_other_pixels = np.zeros((w, h), dtype=bool)
        self.__set_values_from_this(new_self_pixels, - h1/2, h1/2, -w1/2, w1/2)
        other.__set_values_from_this(new_other_pixels, -h2/2, h2/2, -w2/2, w2/2)
        return np.all(new_self_pixels == new_other_pixels)

    def width(self) -> float:
        return self.pixels.shape[0]

    def height(self) -> float:
        return self.pixels.shape[1]

    def isEmpty(self) -> bool:
        return not self.pixels.any()

    def dim(self) -> tuple[float, float]:
        return self.pixels.shape

    def toImage(self, name="default.bmp"):
        img = Image.fromarray(np.uint8(np.where(self.pixels, 0, 255)), 'L')
        img.save('resources/' + name)
