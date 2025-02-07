import numpy as np
from math import ceil
from numpy import unravel_index, rot90, zeros

from src.birectangle import BiRectangle
from src.point import Point
from src.rectangle import Rectangle
from src.shapes.shape import Shape
from src.utils import image_to_array, arr_set_range_value_from_array
import largestinteriorrectangle as lir

class PixelShape(Shape):

    def getOuterRectangle(self) -> Rectangle:
        if self.outerRectangle is None:
            w, h = self.pixels.shape
            ind = unravel_index(self.pixels.argmax(), self.pixels.shape)[0]
            y_min = ind - w / 2
            temp = rot90(self.pixels[ind:])
            ind = unravel_index(temp.argmax(), temp.shape)[0]
            x_max = (h - ind) - h / 2
            temp = rot90(temp[ind:])
            ind = unravel_index(temp.argmax(), temp.shape)[0]
            y_max = (w - ind) - w / 2
            temp = rot90(temp[ind:])
            x_min = unravel_index(temp.argmax(), temp.shape)[0] - h / 2
            self.outerRectangle = Rectangle(x_min, x_max, y_min, y_max)
        return self.outerRectangle

    def getInnerRectangle(self) -> Rectangle:
        # find the largest interior rectangle
        topLeft_x, topLeft_y, w, h = lir.lir(self.pixels)
        w2, h2 = self.pixels.shape
        # have to adjust because we consider the center of the image to be the origin
        return Rectangle.fromTopLeft(Point(topLeft_x - h2/2, topLeft_y + h - w2/2), w, h)

    def __init__(self, img=None, array=None):
        if img is not None:
            self.pixels = image_to_array(img)
        elif array is not None:
            self.pixels = array

        self.outerRectangle = None

    @staticmethod
    def fromRectangles(rectangles):
        r0 = rectangles[0]
        w, h = ceil(max(2 * abs(r0.y_min), 2 * abs(r0.y_max))), ceil(max(2 * abs(r0.x_min), 2 * abs(r0.x_max)))
        array = zeros((w, h), dtype=bool)
        array[int(r0.y_min + w / 2):int(r0.y_max + w / 2), int(r0.x_min + h / 2):int(r0.x_max + h / 2)] = True

        for r in rectangles[1:]:
            a_w, a_h = array.shape
            w, h = (ceil(max(2 * abs(r.y_min), 2 * abs(r.y_max), a_w)),
                    ceil(max(2 * abs(r.x_min), 2 * abs(r.x_max), a_h)))
            if w != a_w or h != a_h:
                array = zeros((w, h), dtype=bool)
                array[int((w - a_w) / 2):int((w + a_w) / 2), int((h - a_h) / 2):int((h + a_h) / 2)] = array
            array[int(r.y_min + w / 2):int(r.y_max + w / 2), int(r.x_min + h / 2):int(r.x_max + h / 2)] = True

        return PixelShape(array=array)

    @staticmethod
    def fromShape(pixel_shape, x_min, x_max, y_min, y_max):
        array = np.zeros((ceil(max(2 * abs(y_min), 2 * abs(y_max))),
                                ceil(max(2 * abs(x_min), 2 * abs(x_max)))), dtype=bool)
        print(array.shape)
        arr_set_range_value_from_array(array, x_min, x_max, y_min, y_max, pixel_shape.pixels)
        return PixelShape(array=array)

    def color(self, x, y):
        return self.pixels[int(y + self.get_width() / 2)][int(x + self.get_height() / 2)]

    def get_width(self):
        return self.pixels.shape[0]

    def get_height(self):
        return self.pixels.shape[1]

    # one of the ways to cut
    # #################
    # #     |         #
    # #  1  |    2    #
    # #     #####-----#
    # #     #   #     #
    # #-----#####     #
    # #    3    |  4  #
    # #         |     #
    # #################
    def cutting_in_4(self, birectangle: BiRectangle):
        big_r = birectangle.outerRectangle
        little_r = birectangle.innerRectangle
        new_shapes = [PixelShape.fromShape(self, big_r.x_min, little_r.x_min, big_r.y_min, little_r.y_max),
                      PixelShape.fromShape(self, little_r.x_min, big_r.x_max, big_r.y_min, little_r.y_min),
                      PixelShape.fromShape(self, big_r.x_min, little_r.x_max, little_r.y_max, big_r.y_max),
                      PixelShape.fromShape(self, little_r.x_max, big_r.x_max, little_r.y_min, big_r.y_max)]
        return new_shapes

    # one of the ways to cut
        # #################
        # #     |   |     #
        # #  1  | 2 |  3  #
        # #-----#####-----#
        # #  4  #   #  5  #
        # #-----#####-----#
        # #  6  | 7 |  8  #
        # #     |   |     #
        # #################
    def cutting_in_8(self, birectangle):
        big_r = birectangle.outerRectangle
        little_r = birectangle.innerRectangle
        new_shapes = [PixelShape.fromShape(self, big_r.x_min, little_r.x_min, big_r.y_min, little_r.y_min),
                      PixelShape.fromShape(self, little_r.x_min, little_r.x_max, big_r.y_min, little_r.y_min),
                      PixelShape.fromShape(self, little_r.x_max, big_r.x_max, big_r.y_min, little_r.y_min),
                      PixelShape.fromShape(self, big_r.x_min, little_r.x_min, little_r.y_min, little_r.y_max),
                      PixelShape.fromShape(self, little_r.x_max, big_r.x_max, little_r.y_min, little_r.y_max),
                      PixelShape.fromShape(self, big_r.x_min, little_r.x_min, little_r.y_max, big_r.y_max),
                      PixelShape.fromShape(self, little_r.x_min, little_r.x_max, little_r.y_max, big_r.y_max),
                      PixelShape.fromShape(self, little_r.x_max, big_r.x_max, little_r.y_max, big_r.y_max)]
        return new_shapes

    def isblank(self) -> bool:
        return not self.pixels.any()
