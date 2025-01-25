import numpy as np
from PIL import Image
from copy import copy
from math import ceil
from numpy import unravel_index, rot90, zeros

from src.birectangle import BiRectangle
from src.rectangle import Rectangle
from src.point import Point
from src.shapes.shape import Shape
from src.utils.constants import *
from src.utils.utils import aux, find_unique_bool


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
        pass

    def __init__(self, img=None, pixel_shape=None, x_min=None, x_max=None, y_min=None, y_max=None, array=None):
        # Black -> True
        # White (and everything else) -> False
        if img is not None:
            self.pixels = np.where(np.array(Image.open(img)) == 0, True, False)
        elif pixel_shape is not None:
            self.pixels = np.zeros((ceil(max(2 * abs(y_min), 2 * abs(y_max))),
                                   ceil(max(2 * abs(x_min), 2 * abs(x_max)))), dtype=bool)
            self.set_range_value(x_min, x_max, y_min, y_max, pixel_shape.range(x_min, x_max, y_min, y_max))
        elif array is not None:
            self.pixels = array

        self.outerRectangle = None

    def color(self, x, y) -> bool:
        return self.pixels[int(y + self.get_width() / 2)][int(x + self.get_height() / 2)]

    def range(self, x_min, x_max, y_min, y_max):
        return arr_range(self.pixels, x_min, x_max, y_min, y_max)

    def set_range_value(self, x_min, x_max, y_min, y_max, value):
        arr_set_range_value(self.pixels, x_min, x_max, y_min, y_max, value)

    def row(self, x_min, x_max, y):
        w, h = self.pixels.shape
        return self.pixels[round(y + w / 2), round(x_min + h / 2):round(x_max + h / 2)]

    def col(self, x, y_min, y_max):
        w, h = self.pixels.shape
        return self.pixels[round(y_min + w / 2):round(y_max + w / 2), round(x + h / 2)]

    def get_width(self):
        return self.pixels.shape[0]

    def get_height(self):
        return self.pixels.shape[1]

    # DOESN'T RESPECT THE SPECIFICATION : r must be inside the shape
    def potential_little_rectangles(self):
        res = []
        big_r: Rectangle = self.getOuterRectangle()
        # could be a random point but must be the "same" across the 3 shapes
        # after analysis, this is incorrect because it is specified that little r should be inside the shape
        # the center of the rectangle is not always inside the shape
        center: Point = big_r.center()

        # if the width (resp. height) is odd then the center of the rectangle is inside a pixel
        # if the width (resp. height) is even then the center is between 2 pixels horizontally (resp. vertically)
        _x = (center.x - 0.5,) if big_r.width() % 2 == 1 else (center.x - 1, center.x)
        _y = (center.y - 0.5,) if big_r.height() % 2 == 1 else (center.y - 1, center.y)

        # colors of the pixels around the center (1, 2 or 4 pixels)
        colors = tuple(self.color(a, b) for a in _x for b in _y)

        if len(colors) < 4:
            same_row_color = len(_y) == 2
            same_column_color = len(_x) == 2
        else:
            same_row_color = colors[0] == colors[2] == 1 and colors[1] == colors[3] == 1
            same_column_color = colors[0] == colors[1] == 1 and colors[2] == colors[3] == 1

        # either we are not in the middle of 4 pixels, or we do but all the 4 pixels have the same color
        if len(colors) < 4 or same_row_color or same_column_color:
            # same colors, so only one rectangle to create
            if all(c == colors[0] == 1 for c in colors):
                res.extend(
                    extend(self, Rectangle(_x[0], _x[-1] + 1, _y[0], _y[-1] + 1), LEFT_RIGHT_UP_DOWN, 4))
            # columns of same color but different colors per columns
            elif same_column_color:
                res.extend(extend(self, Rectangle(_x[0], _x[0] + 1, _y[0], _y[-1] + 1), LEFT_UP_DOWN, 3))
                res.extend(extend(self, Rectangle(_x[1], _x[1] + 1, _y[0], _y[-1] + 1), RIGHT_UP_DOWN, 3))
            else:  # rows of same color but different colors per rows
                res.extend(extend(self, Rectangle(_x[0], _x[-1] + 1, _y[0], _y[0] + 1), LEFT_RIGHT_UP, 3))
                res.extend(
                    extend(self, Rectangle(_x[0] + 1, _x[-1] + 1, _y[1], _y[1] + 1), LEFT_RIGHT_DOWN, 3))
        else:
            index = find_unique_bool(colors)
            _corner = CORNERS[index] if index else None
            # this means there is one of the 4 pixels with a different color than the other ones (= corner)
            if _corner:
                a, b = aux(_corner)
                # extension from the corner with a different color
                if colors[index]:
                    res.extend(extend(self, Rectangle(_x[a], _x[a] + 1, _y[b], _y[b] + 1), _corner, 2))
                # extension from the 2 rectangles formed by the 3 other pixels
                # we just take the color of a different pixel than `corner`
                if colors[index - 1]:
                    res.extend(extend(self, Rectangle(_x[a - 1], _x[a - 1] + 1, _y[0], _y[1] + 1),
                                      LEFT_RIGHT_UP_DOWN - (_corner & LEFT_RIGHT), 3))
                    res.extend(extend(self, Rectangle(_x[0], _x[1] + 1, _y[b - 1], _y[b - 1] + 1),
                                      LEFT_RIGHT_UP_DOWN - (_corner & UP_DOWN), 3))
            else:
                for i in range(len(colors)):
                    a, b = aux(CORNERS[i])
                    if colors[i]:
                        res.extend(extend(self, Rectangle(_x[a], _x[a] + 1, _y[b], _y[b] + 1), CORNERS[i], 2))
        return res

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
        new_shapes = []
        if big_r.x_min != little_r.x_min and big_r.y_min != little_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                         y_min=big_r.y_min, y_max=little_r.y_max))
        if little_r.x_min != big_r.x_max and big_r.y_min != little_r.y_min:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_min, x_max=big_r.x_max,
                                         y_min=big_r.y_min, y_max=little_r.y_min))
        if big_r.x_min != little_r.x_max and little_r.y_max != big_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=big_r.x_min, x_max=little_r.x_max,
                                         y_min=little_r.y_max, y_max=big_r.y_max))
        if little_r.x_max != big_r.x_max and little_r.y_min != big_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                                         y_min=little_r.y_min, y_max=big_r.y_max))
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
        new_shapes = []
        if big_r.x_min != little_r.x_min and big_r.y_min != little_r.y_min:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                         y_min=big_r.y_min, y_max=little_r.y_min))
        if big_r.y_min != little_r.y_min:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_min, x_max=little_r.x_max,
                                         y_min=big_r.y_min, y_max=little_r.y_min))
        if little_r.x_max != big_r.x_max and big_r.y_min != little_r.y_min:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                                         y_min=big_r.y_min, y_max=little_r.y_min))
        if big_r.x_min != little_r.x_min:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                         y_min=little_r.y_min, y_max=little_r.y_max))
        if big_r.x_max != little_r.x_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                                         y_min=little_r.y_min, y_max=little_r.y_max))

        if big_r.x_min != little_r.x_min and big_r.y_max != little_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                         y_min=little_r.y_max, y_max=big_r.y_max))
        if big_r.y_max != little_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_min, x_max=little_r.x_max,
                                         y_min=little_r.y_max, y_max=big_r.y_max))
        if little_r.x_max != big_r.x_max and big_r.y_max != little_r.y_max:
            new_shapes.append(PixelShape(pixel_shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                                         y_min=little_r.y_max, y_max=big_r.y_max))
        return new_shapes

    @staticmethod
    def rectangles_to_shape(rectangles):
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

        return PixelShape(array)

    def isblank(self) -> bool:
        return not self.pixels.any()

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


def can_extend(direction: int, sp: PixelShape, r: Rectangle):
    if direction == UP:
        return r.y_min - 1 >= sp.outerRectangle.y_min and np.all(sp.row(r.x_min, r.x_max, r.y_min - 1))
    if direction == LEFT:
        return r.x_min - 1 >= sp.outerRectangle.x_min and np.all(sp.col(r.x_min - 1, r.y_min, r.y_max))
    if direction == DOWN:
        return r.y_max < sp.outerRectangle.y_max and np.all(sp.row(r.x_min, r.x_max, r.y_max))
    if direction == RIGHT:
        return r.x_max < sp.outerRectangle.x_max and np.all(sp.col(r.x_max, r.y_min, r.y_max))


def corner(_corner: int, r: Rectangle):
    return (r.x_min - 1 if (_corner & LEFT) == LEFT else r.x_max,
            r.y_min - 1 if (_corner & UP) == UP else r.y_max)


def extend(sp: PixelShape, r: Rectangle, sides: int, nb: int, check=True):
    if nb == 0:
        return [r]
    res = []
    if nb == 1:
        if not check:
            r.extend(sides)
        while can_extend(sides, sp, r):
            r.extend(sides)
        res.append(r)
    elif nb == 2:
        if sides == LEFT_RIGHT or sides == UP_DOWN:
            s1 = sides & LEFT_UP
            s2 = sides & RIGHT_DOWN
            if not check:
                r.extend(s1).extend(s2)
            while can_extend(s1, sp, r):
                r.extend(s1)
            while can_extend(s2, sp, r):
                r.extend(s2)
            res.append(r)
        else:
            s1 = sides & LEFT_RIGHT
            s2 = sides & UP_DOWN
            can_ext_1 = not check or can_extend(s1, sp, r)
            can_ext_2 = not check or can_extend(s2, sp, r)
            if can_ext_1 and can_ext_2 and sp.color(*corner(sides, r)) == 1:
                res.extend(extend(sp, r.extend(sides), sides, nb))
            elif can_ext_1 and can_ext_2:
                res.extend(extend(sp, copy(r).extend(s1), s1, 1))
                res.extend(extend(sp, r.extend(s2), s2, 1))
            else:
                while can_ext_1:
                    can_ext_1 = can_extend(s1, sp, r.extend(s1))
                while can_ext_2:
                    can_ext_2 = can_extend(s2, sp, r.extend(s2))
                res.append(r)
    elif nb == 3:
        if check:
            for x in DIRECTIONS:
                if (sides & x) and not can_extend(x, sp, r):
                    sides -= x
                    nb -= 1
        if nb != 3:
            res.extend(extend(sp, r, sides, nb, False))
        else:  # can be extended from every side
            opposites = UP_DOWN if (sides & UP_DOWN) == UP_DOWN else LEFT_RIGHT
            between = sides - opposites
            corner1 = (opposites & RIGHT_DOWN) | between
            corner2 = (opposites & LEFT_UP) | between
            can_ext_corner1 = sp.color(*corner(corner1, r)) == 1
            can_ext_corner2 = sp.color(*corner(corner2, r)) == 1
            if can_ext_corner1 and can_ext_corner2:
                res.extend(extend(sp, r.extend(sides), sides, nb))
            else:
                r2 = copy(r)
                res.extend(extend(sp, r2.extend(opposites), opposites, 2))
                if can_ext_corner1:
                    res.extend(extend(sp, r.extend(corner1), corner1, 2))
                elif can_ext_corner2:
                    res.extend(extend(sp, r.extend(corner2), corner2, 2))
                else:
                    res.extend(extend(sp, r.extend(between), between, 1))
                res.append(r)
                res.append(r2)
    else:  # check is always True
        for x in DIRECTIONS:
            if not can_extend(x, sp, r):
                sides -= x
                nb -= 1
        if nb != 4:
            res.extend(extend(sp, r, sides, nb, False))
        else:
            can_ext = tuple(sp.color(*corner(y, r)) == 1 for y in CORNERS)
            nb_true = can_ext.count(True)
            if nb_true == 0:
                res.extend(extend(sp, copy(r).extend(LEFT_RIGHT), LEFT_RIGHT, 2))
                res.extend(extend(sp, r.extend(UP_DOWN), UP_DOWN, 2))
            elif nb_true == 1:
                index = find_unique_bool(can_ext)
                res.extend(extend(sp, r.extend(CORNERS[index]), CORNERS[index], 2))
            elif nb_true == 2:
                corner1, corner2 = (CORNERS[i] for i in range(4) if can_ext[i])
                if (corner1 | corner2) == LEFT_RIGHT_UP_DOWN:
                    res.extend(extend(sp, copy(r).extend(corner1), corner1, 2))
                    res.extend(extend(sp, r.extend(corner2), corner2, 2))
                else:
                    res.extend(extend(sp, copy(r).extend(corner1 | corner2), corner1 | corner2, 3))
                    s = LEFT_RIGHT_UP_DOWN - (corner1 ^ corner2)
                    res.extend(extend(sp, r.extend(s), s, 2))
            elif nb_true == 3:
                index = find_unique_bool(can_ext)
                d1 = LEFT_RIGHT_UP_DOWN - (CORNERS[index] & LEFT_RIGHT)
                res.extend(extend(sp, copy(r).extend(d1), d1, 3))
                d2 = LEFT_RIGHT_UP_DOWN - (CORNERS[index] & UP_DOWN)
                res.extend(extend(sp, r.extend(d2), d2, 3))
            else:
                res.extend(extend(sp, r.extend(sides), sides, 4))
    return res