from point import Point
from utils.constants import LEFT, RIGHT, UP, DOWN


class Rectangle:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def get_width(self) -> int:
        return self.x_max - self.x_min

    def get_height(self) -> int:
        return self.y_max - self.y_min

    def get_center(self) -> Point:
        return Point((self.x_max+self.x_min)/2, (self.y_max+self.y_min)/2)

    def get_up_left(self) -> Point:
        return Point(self.x_min, self.y_min)

    def get_up_right(self) -> Point:
        return Point(self.x_max, self.y_min)

    def get_bottom_left(self) -> Point:
        return Point(self.x_min, self.y_max)

    def get_bottom_right(self) -> Point:
        return Point(self.x_max, self.y_max)

    def get_area(self):
        return self.get_width() * self.get_height()

    def extend(self, direction):
        if direction & UP == UP:
            self.y_min -= 1
        if direction & LEFT == LEFT:
            self.x_min -= 1
        if direction & DOWN == DOWN:
            self.y_max += 1
        if direction & RIGHT == RIGHT:
            self.x_max += 1
        return self


    def __repr__(self):
        return f"{self.get_up_left()}, {self.get_bottom_right()}"
        # return f"center : {self.get_center()}, dim : {self.get_width()}×{self.get_height()}"

def rectangle_analogy(r_a: Rectangle, r_b: Rectangle, r_c: Rectangle):
    center_a = r_a.get_center()
    center_b = r_b.get_center()
    center_c = r_c.get_center()
    center_d = (center_c.x + (center_b.x - center_a.x), center_c.y + (center_b.y - center_a.y))
    w_d = r_c.get_width() * (r_b.get_width() / r_a.get_width())
    h_d = r_c.get_height() * (r_b.get_height() / r_a.get_height())
    return Rectangle(center_d[0] - w_d / 2, center_d[0] + w_d / 2,
                     center_d[1] - h_d / 2, center_d[1] + h_d / 2)

def greatest_common_rectangle_ratio(r_a: Rectangle, big_r_a: Rectangle, r_b: Rectangle, big_r_b: Rectangle,
                                    r_c: Rectangle, big_r_c: Rectangle):
    w_a, h_a = big_r_a.get_width(), big_r_a.get_height()
    w_b, h_b = big_r_b.get_width(), big_r_b.get_height()
    w_c, h_c = big_r_c.get_width(), big_r_c.get_height()
    r_x_min = max((r_a.x_min - big_r_a.x_min) / w_a, (r_b.x_min - big_r_b.x_min) / w_b,
                  (r_c.x_min - big_r_c.x_min) / w_c)
    r_x_max = min((big_r_a.x_max - r_a.x_max) / w_a, (big_r_b.x_max - r_b.x_max) / w_b,
                  (big_r_c.x_max - r_c.x_max) / w_c)
    r_y_min = max((r_a.y_min - big_r_a.y_min) / h_a, (r_b.y_min - big_r_b.y_min) / h_b,
                  (r_c.y_min - big_r_c.y_min) / h_c)
    r_y_max = min((big_r_a.y_max - r_a.y_max) / h_a, (big_r_b.y_max - r_b.y_max) / h_b,
                  (big_r_c.y_max - r_c.y_max) / h_c)

    return r_x_min, r_x_max, r_y_min, r_y_max