import numpy as np
from PIL import Image
from copy import copy

from src.rectangle import Rectangle, rectangle_analogy, greatest_common_rectangle_ratio
from src.point import Point
from src.utils.constants import *
from src.utils.utils import aux, find_unique_bool


class Shape:
    def __init__(self, img=None, shape=None, x_min=None, x_max=None, y_min=None, y_max=None, big_r=None):
        # Black -> True
        # White (and everything else) -> False
        if img:
            img = Image.open(img)
            tab = np.array(img)
            self.shape = np.zeros(tab.shape[:2], dtype=bool)
            # Compare each pixel with black color and assign 1 where they are equal
            self.shape[np.all(tab == [0, 0, 0], axis=-1)] = True
        else:
            if x_min:
                self.shape = shape[y_min:y_max, x_min:x_max]
            else:
                self.shape = shape

        self.big_r = big_r if big_r else self.find_big_rectangle()
        self.little_r = None

    def find_big_rectangle(self):
        if self.shape.any():
            w, h = self.shape.shape
            y_min, offset = np.unravel_index(self.shape.argmax(), self.shape.shape)
            temp = np.rot90(self.shape[offset:])
            ind, offset = np.unravel_index(temp.argmax(), temp.shape)
            x_max = w - ind
            temp = np.rot90(temp[:, :w - offset])
            ind, offset = np.unravel_index(temp.argmax(), temp.shape)
            y_max = h - ind
            temp = np.rot90(temp[:h - offset])
            x_min = np.unravel_index(temp.argmax(), temp.shape)[0]
            return Rectangle(x_min, x_max, y_min, y_max)
        else:
            return None

    def color(self, x, y) -> bool:
        return self.shape[int(y)][int(x)]

    def get_width(self):
        return self.shape.shape[0]

    def get_height(self):
        return self.shape.shape[1]

    def big_rectangle(self):
        return self.big_r

    # we assume every pixel of the rectangle has the same color
    def get_color_little_rectangle(self):
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
        new_shape1 = Shape(shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                           y_min=big_r.y_min, y_max=little_r.y_max)
        new_shape2 = Shape(shape=self, x_min=little_r.x_min, x_max=big_r.x_max,
                           y_min=big_r.y_min, y_max=little_r.y_min)
        new_shape3 = Shape(shape=self, x_min=big_r.x_min, x_max=little_r.x_min,
                           y_min=little_r.y_max, y_max=big_r.y_max)
        new_shape4 = Shape(shape=self, x_min=little_r.x_max, x_max=big_r.x_max,
                           y_min=little_r.y_min, y_max=big_r.y_max)
        return new_shape1, new_shape2, new_shape3, new_shape4


def to_image(array, name="default.bmp"):
    pixel_array = np.full((array.shape[0], array.shape[1], 3), 255, dtype=np.uint8)
    pixel_array[array] = [0, 0, 0]
    img = Image.fromarray(pixel_array)
    img.save(name)


def can_extend(direction: int, color: bool, shape: Shape, r: Rectangle):
    if direction == UP:
        return r.y_min >= 1 and np.all(shape.shape[int(r.y_min - 1), int(r.x_min):int(r.x_max)] == color)
    if direction == LEFT:
        return r.x_min >= 1 and np.all(shape.shape[int(r.y_min):int(r.y_max), int(r.x_min - 1)] == color)
    if direction == DOWN:
        return r.y_max < shape.get_height() and np.all(shape.shape[int(r.y_max), int(r.x_min):int(r.x_max)] == color)
    if direction == RIGHT:
        return r.x_max < shape.get_width() and np.all(shape.shape[int(r.y_min):int(r.y_max), int(r.x_max)] == color)


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


def find_real_little_rectangles(little_r_a_candidates, big_r_a, little_r_b_candidates, big_r_b,
                           little_r_c_candidates, big_r_c, big_r_d):
    w_big_r_d, h_big_r_d = big_r_d.get_width(), big_r_d.get_height()
    chosen = None
    area_max = 0
    # we are going to take the rectangles maximising the area of the little rectangle of d
    for candidate_r_a in little_r_a_candidates:
        for candidate_r_b in little_r_b_candidates:
            for candidate_r_c in little_r_c_candidates:
                r_x_min, r_x_max, r_y_min, r_y_max = greatest_common_rectangle_ratio(candidate_r_a, big_r_a,
                                                                                     candidate_r_b, big_r_b,
                                                                                     candidate_r_c, big_r_c)
                d_x_min = big_r_d.x_min + w_big_r_d * r_x_min
                d_x_max = big_r_d.x_max - w_big_r_d * r_x_max
                d_y_min = big_r_d.y_min + w_big_r_d * r_y_min
                d_y_max = big_r_d.y_max - w_big_r_d * r_y_max
                area = d_x_max - d_x_min * d_y_max - d_y_min
                if area > area_max:
                    chosen = [candidate_r_a, candidate_r_b, candidate_r_c]
                    area_max = area
    return chosen

# DOESN'T WORK DON'T EXECUTE
def shape_analogy(sp_a: Shape, sp_b: Shape, sp_c: Shape):
    big_r_a = sp_a.big_rectangle()
    big_r_b = sp_b.big_rectangle()
    big_r_c = sp_c.big_rectangle()
    big_r_d = rectangle_analogy(big_r_a, big_r_b, big_r_c)

    little_r_a_candidates = sp_a.potential_little_rectangles()
    little_r_b_candidates = sp_b.potential_little_rectangles()
    little_r_c_candidates = sp_c.potential_little_rectangles()

    sp_a.little_r, sp_b.little_r, sp_c.little_r = find_real_little_rectangles(little_r_a_candidates, big_r_a,
                                                                              little_r_b_candidates, big_r_b,
                                                                              little_r_c_candidates, big_r_c, big_r_d)
    color_c = sp_c.get_color_little_rectangle()
    little_r_d_color = color_c if sp_a.get_color_little_rectangle() == sp_b.get_color_little_rectangle() else not color_c
    little_r_d = rectangle_analogy(sp_a.little_r, sp_b.little_r, sp_c.little_r)
    shape_d_w = max(sp_a.get_width(), sp_b.get_width(), sp_c.get_width(), )
    shape_d_h = max(sp_a.get_height(), sp_b.get_height(), sp_c.get_height(), big_r_d.get_height())
    d_array = np.zeros((big_r_d.get_width(), shape_d_h), dtype=bool)
    if little_r_d_color:
        d_array[little_r_d.y_min:little_r_d.y_max, little_r_d.x_min:little_r_d.x_max] = True
    sp_a1, sp_a2, sp_a3, sp_a4 = sp_a.cutting_in_4()
    sp_b1, sp_b2, sp_b3, sp_b4 = sp_b.cutting_in_4()
    sp_c1, sp_c2, sp_c3, sp_c4 = sp_c.cutting_in_4()

    sp_d1 = shape_analogy(sp_a1, sp_b1, sp_c1)
    sp_d2 = shape_analogy(sp_a2, sp_b2, sp_c2)
    sp_d3 = shape_analogy(sp_a3, sp_b3, sp_c3)
    sp_d4 = shape_analogy(sp_a4, sp_b4, sp_c4)
    # HELPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    # depends on the cutting method

    return d_array



