from src.point import Point
from src.utils.constants import LEFT, RIGHT, UP, DOWN


class Rectangle:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def get_width(self) -> int:
        return abs(self.x_max - self.x_min)

    def get_height(self) -> int:
        return abs(self.y_max - self.y_min)

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

    def rectangle_from_ratios(self, r_x_min, r_x_max, r_y_min, r_y_max):
        w, h = self.get_width(), self.get_height()
        x_min = self.x_min + w * r_x_min
        x_max = self.x_max - w * r_x_max
        y_min = self.y_min + h * r_y_min
        y_max = self.y_max - h * r_y_max
        return Rectangle(x_min, x_max, y_min, y_max)

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

    def __eq__(self, other):
        return (isinstance(other, Rectangle) and self.x_min == other.x_min and self.x_max == other.x_max
                and self.y_min == other.y_min and self.y_max == other.y_max)

    def __repr__(self):
        return f"{self.get_up_left()}, {self.get_bottom_right()}"
        # return f"center : {self.get_center()}, dim : {round(self.get_width(), 4)}×{round(self.get_height(), 4)}"


def rectangle_analogy(r_a: Rectangle, r_b: Rectangle, r_c: Rectangle):
    center_a = r_a.get_center()
    center_b = r_b.get_center()
    center_c = r_c.get_center()
    r_w = r_c.get_width() / r_a.get_width()
    r_h = r_c.get_height() / r_a.get_height()
    center_d = (r_w * (center_b.x - center_a.x) + center_c.x, r_h * (center_b.y - center_a.y) + center_c.y)
    w_d = r_c.get_width() * r_b.get_width() / r_a.get_width()
    h_d = r_c.get_height() * r_b.get_height() / r_a.get_height()
    return Rectangle(center_d[0] - w_d / 2, center_d[0] + w_d / 2,
                     center_d[1] - h_d / 2, center_d[1] + h_d / 2)


def greatest_common_rectangle_ratio(r_a: Rectangle, big_r_a: Rectangle, r_b: Rectangle, big_r_b: Rectangle,
                                    r_c: Rectangle, big_r_c: Rectangle):
    w_a, h_a = big_r_a.get_width(), big_r_a.get_height()
    w_b, h_b = big_r_b.get_width(), big_r_b.get_height()
    w_c, h_c = big_r_c.get_width(), big_r_c.get_height()
    r_x_min = max((r_a.x_min - big_r_a.x_min) / w_a, (r_b.x_min - big_r_b.x_min) / w_b,
                  (r_c.x_min - big_r_c.x_min) / w_c)
    r_x_max = max((big_r_a.x_max - r_a.x_max) / w_a, (big_r_b.x_max - r_b.x_max) / w_b,
                  (big_r_c.x_max - r_c.x_max) / w_c)
    r_y_min = max((r_a.y_min - big_r_a.y_min) / h_a, (r_b.y_min - big_r_b.y_min) / h_b,
                  (r_c.y_min - big_r_c.y_min) / h_c)
    r_y_max = max((big_r_a.y_max - r_a.y_max) / h_a, (big_r_b.y_max - r_b.y_max) / h_b,
                  (big_r_c.y_max - r_c.y_max) / h_c)
    return r_x_min, r_x_max, r_y_min, r_y_max


def find_little_rectangles(little_r_a_candidates, big_r_a, little_r_b_candidates, big_r_b,
                           little_r_c_candidates, big_r_c, big_r_d):
    chosen = best_r_d = None
    area_max = 0
    # we are going to take the rectangles maximising the area of the little rectangle of d
    for candidate_r_a in little_r_a_candidates:
        for candidate_r_b in little_r_b_candidates:
            for candidate_r_c in little_r_c_candidates:
                r_x_min, r_x_max, r_y_min, r_y_max = greatest_common_rectangle_ratio(candidate_r_a, big_r_a,
                                                                                     candidate_r_b, big_r_b,
                                                                                     candidate_r_c, big_r_c)
                r_d = big_r_d.rectangle_from_ratios(r_x_min, r_x_max, r_y_min, r_y_max)
                area = r_d.get_area()
                if area > area_max:
                    chosen = r_x_min, r_x_max, r_y_min, r_y_max
                    area_max = area
                    best_r_d = r_d
    return [big_r_a.rectangle_from_ratios(*chosen), big_r_b.rectangle_from_ratios(*chosen),
            big_r_c.rectangle_from_ratios(*chosen), best_r_d]