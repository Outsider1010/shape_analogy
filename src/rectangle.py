from src.point import Point


class Rectangle:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.w = self.width()
        self.h = self.height()

    def width(self) -> int:
        return self.x_max - self.x_min

    def height(self) -> int:
        return self.y_max - self.y_min

    def center(self) -> Point:
        return Point((self.x_max + self.x_min) / 2, (self.y_max + self.y_min) / 2)

    def topLeft(self) -> Point:
        return Point(self.x_min, self.y_max)

    def topRight(self) -> Point:
        return Point(self.x_max, self.y_max)

    def bottomLeft(self) -> Point:
        return Point(self.x_min, self.y_min)

    def bottomRight(self) -> Point:
        return Point(self.x_max, self.y_min)

    def area(self):
        return self.width() * self.height()

    def rectangle_from_ratios(self, r_x_min, r_x_max, r_y_min, r_y_max):
        w, h = self.width(), self.height()
        x_min = self.x_min + w * r_x_min
        x_max = self.x_max - w * r_x_max
        y_min = self.y_min + h * r_y_min
        y_max = self.y_max - h * r_y_max
        return Rectangle(x_min, x_max, y_min, y_max)

    def __eq__(self, other):
        return (isinstance(other, Rectangle) and self.x_min == other.x_min and self.x_max == other.x_max
                and self.y_min == other.y_min and self.y_max == other.y_max)

    def __repr__(self):
        # return f"{self.bottomLeft()}, {self.topRight()}"
        return f"topLeft={self.topLeft()}, w={round(self.width(), 4)}, h={round(self.height(), 4)}"

    @staticmethod
    def fromCenter(center, w, h):
        return Rectangle(center.x - w/2, center.x + w/2, center.y - h/2, center.y + h/2)

    @staticmethod
    def fromTopLeft(top_left, w, h):
        return Rectangle(top_left.x, top_left.x + w, top_left.y - h, top_left.y)

    @staticmethod
    def analogy(rectangle_a, rectangle_b, rectangle_c):
        center_a = rectangle_a.center()
        center_b = rectangle_b.center()
        center_c = rectangle_c.center()
        center_d = Point.analogy(center_a, center_b, center_c)
        w_d = rectangle_c.width() * rectangle_b.width() / rectangle_a.width()
        h_d = rectangle_c.height() * rectangle_b.height() / rectangle_a.height()
        return Rectangle.fromCenter(center_d, w_d, h_d)

    def containsRectangle(self, r):
        """
        Check if this rectangle contains r
        :param r: inner rectangle
        :return: True if this rectangle contains r
        """
        bottom_condition = self.y_min <= r.y_min
        top_condition = self.y_max >= r.y_max
        left_condition = self.x_min <= r.x_min
        right_condition = self.x_max >= r.x_max
        return bottom_condition and top_condition and left_condition and right_condition


def greatest_common_rectangle_ratio(r_a: Rectangle, big_r_a: Rectangle,
                                    r_b: Rectangle, big_r_b: Rectangle,
                                    r_c: Rectangle, big_r_c: Rectangle):
    w_a, h_a = big_r_a.width(), big_r_a.height()
    w_b, h_b = big_r_b.width(), big_r_b.height()
    w_c, h_c = big_r_c.width(), big_r_c.height()
    r_x_min = max((r_a.x_min - big_r_a.x_min) / w_a, (r_b.x_min - big_r_b.x_min) / w_b,
                  (r_c.x_min - big_r_c.x_min) / w_c)
    r_x_max = max((big_r_a.x_max - r_a.x_max) / w_a, (big_r_b.x_max - r_b.x_max) / w_b,
                  (big_r_c.x_max - r_c.x_max) / w_c)
    r_y_min = max((r_a.y_min - big_r_a.y_min) / h_a, (r_b.y_min - big_r_b.y_min) / h_b,
                  (r_c.y_min - big_r_c.y_min) / h_c)
    r_y_max = max((big_r_a.y_max - r_a.y_max) / h_a, (big_r_b.y_max - r_b.y_max) / h_b,
                  (big_r_c.y_max - r_c.y_max) / h_c)
    return r_x_min, r_x_max, r_y_min, r_y_max