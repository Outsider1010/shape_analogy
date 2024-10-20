import numpy as np
from PIL import Image
from copy import copy
from math import ceil

from src.rectangle import Rectangle, rectangle_analogy, greatest_common_rectangle_ratio
from src.point import Point
from src.utils.constants import *
from src.utils.utils import aux, find_unique_bool


class Shape:
    def __init__(self, img=None, shape=None, x_min=None, x_max=None, y_min=None, y_max=None, array=None):
        # Black -> True
        # White (and everything else) -> False
        if img is not None:
            self.shape = np.where(np.array(Image.open(img)) == 0, True, False)
        elif shape is not None:
            self.shape = shape.range(x_min, x_max, y_min, y_max)
        elif array is not None:
            self.shape = array

        self.big_r = self.find_big_rectangle()
        self.little_r = None

    def find_big_rectangle(self):
        if self.shape.any():
            w, h = self.shape.shape
            ind = np.unravel_index(self.shape.argmax(), self.shape.shape)[0]
            y_min = ind - w/2
            temp = np.rot90(self.shape[ind:])
            ind = np.unravel_index(temp.argmax(), temp.shape)[0]
            x_max = (h - ind) - h/2
            temp = np.rot90(temp[ind:])
            ind = np.unravel_index(temp.argmax(), temp.shape)[0]
            y_max = (w - ind) - w/2
            temp = np.rot90(temp[ind:])
            x_min = np.unravel_index(temp.argmax(), temp.shape)[0] - h/2
            return Rectangle(x_min, x_max, y_min, y_max)
        else:
            return None

    def color(self, x, y) -> bool:
        return self.shape[int(y + self.get_width()/2)][int(x + self.get_height()/2)]

    def range(self, x_min, x_max, y_min, y_max):
        w, h = self.shape.shape
        return self.shape[int(y_min + w/2):int(y_max + w/2), int(x_min + h/2):int(x_max + h/2)]

    def row(self, x, y_min, y_max):
        w, h = self.shape.shape
        return self.shape[int(x + h/2), int(y_min + w / 2):int(y_max + w / 2)]

    def col(self, x_min, x_max, y):
        w, h = self.shape.shape
        return self.shape[int(x_min + h / 2):int(x_max + h / 2), int(y + w / 2)]

    def get_width(self):
        return self.shape.shape[0]

    def get_height(self):
        return self.shape.shape[1]

    def big_rectangle(self):
        return self.big_r

    # we assume every pixel of the rectangle has the same color
    def color_little_rectangle(self):
        return self.color(self.little_r.x_min, self.little_r.y_min)

    def potential_little_rectangles(self):
        res = []
        big_r: Rectangle = self.big_rectangle()
        # could be a random point but must be the "same" across the 3 shapes
        center: Point = big_r.get_center()

        # if the width (resp. height) is odd then the center of the rectangle is inside a pixel
        # if the width (resp. height) is even then the center is between 2 pixels horizontally (resp. vertically)
        _x = (center.x - 0.5,) if big_r.get_width() % 2 == 1 else (center.x - 1, center.x)
        _y = (center.y - 0.5,) if big_r.get_height() % 2 == 1 else (center.y - 1, center.y)

        # colors of the pixels around the center (1, 2 or 4 pixels)
        colors = tuple(self.color(a, b) for a in _x for b in _y)

        if len(colors) < 4:
            same_row_color = same_column_color = True
        else:
            same_row_color = (len(colors) == len(_x) == 2) or (colors[0] == colors[2] and colors[1] == colors[3])
            same_column_color = (len(colors) == len(_y) == 2) or (colors[0] == colors[1] and colors[2] == colors[3])

        # either we are not in the middle of 4 pixels, or we do but all the 4 pixels have the same color
        if len(colors) < 4 or same_row_color or same_column_color:
            # same colors, so only one rectangle to create
            if all(c == colors[0] for c in colors):
                res.extend(
                    extend(self, Rectangle(_x[0], _x[-1] + 1, _y[0], _y[-1] + 1), colors[0], LEFT_RIGHT_UP_DOWN, 4))
            # columns of same color but different colors per columns
            elif same_column_color:
                res.extend(extend(self, Rectangle(_x[0], _x[0] + 1, _y[0], _y[-1] + 1), colors[0], LEFT_UP_DOWN, 3))
                res.extend(extend(self, Rectangle(_x[1], _x[1] + 1, _y[0], _y[-1] + 1), colors[-1], RIGHT_UP_DOWN, 3))
            else:  # rows of same color but different colors per rows
                res.extend(extend(self, Rectangle(_x[0], _x[-1] + 1, _y[0], _y[0] + 1), colors[0], LEFT_RIGHT_UP, 3))
                res.extend(
                    extend(self, Rectangle(_x[0] + 1, _x[-1] + 1, _y[1], _y[1] + 1), colors[1], LEFT_RIGHT_DOWN, 3))
        else:
            index = find_unique_bool(colors)
            _corner = CORNERS[index] if index else None
            # this means there is one of the 4 pixels with a different color than the other ones (= corner)
            if _corner:
                a, b = aux(_corner)
                # extension from the corner with a different color
                res.extend(extend(self, Rectangle(_x[a], _x[a] + 1, _y[b], _y[b] + 1), colors[index], _corner, 2))
                # extension from the 2 rectangles formed by the 3 other pixels
                # we just take the color of a different pixel than `corner`
                res.extend(extend(self, Rectangle(_x[a - 1], _x[a - 1] + 1, _y[0], _y[1] + 1), colors[index - 1],
                                  LEFT_RIGHT_UP_DOWN - (_corner & LEFT_RIGHT), 3))
                res.extend(extend(self, Rectangle(_x[0], _x[1] + 1, _y[b - 1], _y[b - 1] + 1), colors[index - 1],
                                  LEFT_RIGHT_UP_DOWN - (_corner & UP_DOWN), 3))
            else:
                for i in range(len(colors)):
                    a, b = aux(CORNERS[i])
                    res.extend(extend(self, Rectangle(_x[a], _x[a] + 1, _y[b], _y[b] + 1), colors[i], CORNERS[i], 2))
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
    def cutting_in_4(self):
        big_r = self.big_r
        little_r = self.little_r
        new_shapes = []
        if big_r.x_min != little_r.x_min and big_r.y_min != little_r.y_max:
            new_shapes.append(Shape(shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                    y_min=big_r.y_min, y_max=little_r.y_max))
        if little_r.x_min != big_r.x_max and big_r.y_min != little_r.y_min:
            new_shapes.append(Shape(shape=self, x_min=little_r.x_min, x_max=big_r.x_max,
                                    y_min=big_r.y_min, y_max=little_r.y_min))
        if big_r.x_min != little_r.x_min and little_r.y_max != big_r.y_max:
            new_shapes.append(Shape(shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                                    y_min=little_r.y_max, y_max=big_r.y_max))
        if little_r.x_max != big_r.x_max and little_r.y_min != big_r.y_max:
            new_shapes.append(Shape(shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                                    y_min=little_r.y_min, y_max=big_r.y_max))
        return new_shapes


def to_image(array, name="default.bmp"):
    img = Image.fromarray(np.uint8(np.where(array, 0, 255)), 'L')
    img.save('resources/'+name)


def can_extend(direction: int, color: bool, shape: Shape, r: Rectangle):
    if direction == UP:
        return r.y_min + shape.get_height() / 2 >= 1 and np.all(shape.row(r.y_min - 1, r.x_min, r.x_max) == color)
    if direction == LEFT:
        return r.x_min + shape.get_width() / 2 >= 1 and np.all(shape.col(r.y_min, r.y_max, r.x_min - 1) == color)
    if direction == DOWN:
        return r.y_max < shape.get_height()/2 and np.all(shape.row(r.y_max, r.x_min, r.x_max) == color)
    if direction == RIGHT:
        return r.x_max < shape.get_width()/2 and np.all(shape.col(r.y_min, r.y_max, r.x_max) == color)


def corner(_corner: int, r: Rectangle):
    return (r.x_min - 1 if (_corner & LEFT) == LEFT else r.x_max,
            r.y_min - 1 if (_corner & UP) == UP else r.y_max)


def extend(sp: Shape, r: Rectangle, color: bool, sides: int, nb: int, check=True):
    if nb == 0:
        return [r]
    res = []
    if nb == 1:
        if not check:
            r.extend(sides)
        while can_extend(sides, color, sp, r):
            r.extend(sides)
        res.append(r)
    elif nb == 2:
        if sides == LEFT_RIGHT or sides == UP_DOWN:
            s1 = sides & LEFT_UP
            s2 = sides & RIGHT_DOWN
            if not check:
                r.extend(s1).extend(s2)
            while can_extend(s1, color, sp, r):
                r.extend(s1)
            while can_extend(s2, color, sp, r):
                r.extend(s2)
            res.append(r)
        else:
            s1 = sides & LEFT_RIGHT
            s2 = sides & UP_DOWN
            can_ext_1 = not check or can_extend(s1, color, sp, r)
            can_ext_2 = not check or can_extend(s2, color, sp, r)
            if can_ext_1 and can_ext_2 and sp.color(*corner(sides, r)) == color:
                res.extend(extend(sp, r.extend(sides), color, sides, nb))
            elif can_ext_1 and can_ext_2:
                res.extend(extend(sp, copy(r).extend(s1), color, s1, 1))
                res.extend(extend(sp, r.extend(s2), color, s2, 1))
            else:
                while can_ext_1:
                    can_ext_1 = can_extend(s1, color, sp, r.extend(s1))
                while can_ext_2:
                    can_ext_2 = can_extend(s2, color, sp, r.extend(s2))
                res.append(r)
    elif nb == 3:
        if check:
            for x in DIRECTIONS:
                if (sides & x) and not can_extend(x, color, sp, r):
                    sides -= x
                    nb -= 1
        if nb != 3:
            res.extend(extend(sp, r, color, sides, nb, False))
        else:  # can be extended from every side
            opposites = UP_DOWN if (sides & UP_DOWN) == UP_DOWN else LEFT_RIGHT  # up_down
            between = sides - opposites  # right
            corner1 = (opposites & RIGHT_DOWN) + between  # right_down
            corner2 = (opposites & LEFT_UP) + between  # right_up
            can_ext_corner1 = sp.color(*corner(corner1, r)) == color
            can_ext_corner2 = sp.color(*corner(corner2, r)) == color
            if can_ext_corner1 and can_ext_corner2:
                res.extend(extend(sp, r.extend(sides), color, sides, nb))
            else:
                r2 = copy(r)
                res.extend(extend(sp, r2.extend(opposites), color, opposites, 2))
                if can_ext_corner1:
                    res.extend(extend(sp, r.extend(corner1), color, corner1, 2))
                elif can_ext_corner2:
                    res.extend(extend(sp, r.extend(corner2), color, corner2, 2))
                else:
                    res.extend(extend(sp, r.extend(between), color, between, 1))
                res.append(r)
                res.append(r2)
    else:  # check is always True
        for x in DIRECTIONS:
            if not can_extend(x, color, sp, r):
                sides -= x
                nb -= 1
        if nb != 4:
            res.extend(extend(sp, r, color, sides, nb, False))
        else:
            can_ext = tuple(sp.color(*corner(y, r)) == color for y in CORNERS)
            nb_true = can_ext.count(True)
            if nb_true == 0:
                res.extend(extend(sp, copy(r).extend(LEFT_RIGHT), color, LEFT_RIGHT, 2))
                res.extend(extend(sp, r.extend(UP_DOWN), color, UP_DOWN, 2))
            elif nb_true == 1:
                index = find_unique_bool(can_ext)
                res.extend(extend(sp, r.extend(CORNERS[index]), color, CORNERS[index], 2))
            elif nb_true == 2:
                corner1, corner2 = (CORNERS[i] for i in range(4) if can_ext[i])
                if corner1 + corner2 == LEFT_RIGHT_UP_DOWN:
                    res.extend(extend(sp, copy(r).extend(corner1), color, corner1, 2))
                    res.extend(extend(sp, r.extend(corner2), color, corner2, 2))
                else:
                    res.extend(extend(sp, r.extend(corner1 + corner2), color, corner1 + corner2, 3))
            elif nb_true == 3:
                index = find_unique_bool(can_ext)
                d1 = LEFT_RIGHT_UP_DOWN - (CORNERS[index] & LEFT_RIGHT)
                res.extend(extend(sp, copy(r).extend(d1), color, d1, 3))
                d2 = LEFT_RIGHT_UP_DOWN - (CORNERS[index] & UP_DOWN)
                res.extend(extend(sp, r.extend(d2), color, d2, 3))
            else:
                res.extend(extend(sp, r.extend(sides), color, sides, 4))
    return res


def rectangle_from_ratios(big_r, r_x_min, r_x_max, r_y_min, r_y_max):
    w, h = big_r.get_width(), big_r.get_height()
    x_min = big_r.x_min + w * r_x_min
    x_max = big_r.x_max - w * r_x_max
    y_min = big_r.y_min + h * r_y_min
    y_max = big_r.y_max - h * r_y_max
    return x_min, x_max, y_min, y_max


def find_little_rectangles(little_r_a_candidates, big_r_a, little_r_b_candidates, big_r_b,
                           little_r_c_candidates, big_r_c, big_r_d):
    chosen = None
    area_max = 0
    # we are going to take the rectangles maximising the area of the little rectangle of d
    for candidate_r_a in little_r_a_candidates:
        for candidate_r_b in little_r_b_candidates:
            for candidate_r_c in little_r_c_candidates:
                r_x_min, r_x_max, r_y_min, r_y_max = greatest_common_rectangle_ratio(candidate_r_a, big_r_a,
                                                                                     candidate_r_b, big_r_b,
                                                                                     candidate_r_c, big_r_c)
                d_x_min, d_x_max, d_y_min, d_y_max = rectangle_from_ratios(big_r_d, r_x_min, r_x_max, r_y_min, r_y_max)
                area = abs(d_x_max - d_x_min) * abs(d_y_max - d_y_min)
                if area > area_max:
                    chosen = r_x_min, r_x_max, r_y_min, r_y_max
                    area_max = area
    return [Rectangle(*rectangle_from_ratios(big_r_a, *chosen)), Rectangle(*rectangle_from_ratios(big_r_b, *chosen)),
            Rectangle(*rectangle_from_ratios(big_r_c, *chosen)), Rectangle(*rectangle_from_ratios(big_r_d, *chosen))]

# DOESN'T WORK DON'T EXECUTE
def shape_analogy(sp_a: Shape, sp_b: Shape, sp_c: Shape):
    if sp_a.big_r is None or sp_b.big_r is None or sp_c.big_r is None:
        # cas de base
        print("SAIS PAS FAIRE")
        exit()
    else:
        big_r_a = sp_a.big_rectangle()
        big_r_b = sp_b.big_rectangle()
        big_r_c = sp_c.big_rectangle()
        big_r_d = rectangle_analogy(big_r_a, big_r_b, big_r_c)

        little_r_a_candidates = sp_a.potential_little_rectangles()
        little_r_b_candidates = sp_b.potential_little_rectangles()
        little_r_c_candidates = sp_c.potential_little_rectangles()
        sp_a.little_r, sp_b.little_r, sp_c.little_r, little_r_d = find_little_rectangles(little_r_a_candidates, big_r_a,
                                                                                         little_r_b_candidates, big_r_b,
                                                                                         little_r_c_candidates, big_r_c,
                                                                                         big_r_d)
        color_c = sp_c.color_little_rectangle()
        little_r_d_color = color_c if sp_a.color_little_rectangle() == sp_b.color_little_rectangle() else not color_c
        sous_sp_a = sp_a.cutting_in_4()
        sous_sp_b = sp_b.cutting_in_4()
        sous_sp_c = sp_c.cutting_in_4()

        # analogy between rectangles for example
        if len(sous_sp_a) == 0:
            shape_d_w = ceil(max(sp_c.get_width(), sp_b.get_width(), 2 * abs(big_r_d.y_min), 2 * abs(big_r_d.y_max)))
            shape_d_h = ceil(max(sp_c.get_height(), sp_b.get_height(), 2 * abs(big_r_d.x_min), 2 * abs(big_r_d.x_max)))
            d_array = np.zeros((shape_d_w, shape_d_h), dtype=bool)
            if little_r_d_color:
                d_array[int(little_r_d.y_min + shape_d_w/2):int(little_r_d.y_max + shape_d_w/2),
                int(little_r_d.x_min + shape_d_h/2):int(little_r_d.x_max + shape_d_h/2)] = True
            print("R_d (exact) :", big_r_d)
            return Shape(array=d_array)
        else:
            print("SAIS PAS FAIRE 2")
            exit()

def shape_analogy_from_file(img_a: str, img_b: str, img_c: str, name_img_res='default.bmp'):
    sp_a = Shape(img=img_a)
    sp_b = Shape(img=img_b)
    sp_c = Shape(img=img_c)
    res = shape_analogy(sp_a, sp_b, sp_c)
    print("R_a :", sp_a.big_r)
    print("R_b :", sp_b.big_r)
    print("R_c :", sp_c.big_r)
    print("R_d (pixel) :", res.big_r)
    to_image(res.shape, name_img_res)