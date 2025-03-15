from decimal import Decimal

from matplotlib import pyplot as plt

from src.birectangle.Point import Point


class Rectangle:
    """
    An axis-aligned rectangle
    """
    def __init__(self, x_min: Decimal | float, x_max: Decimal | float, y_min: Decimal | float, y_max: Decimal | float):
        prec = Decimal('0.0000001')
        if isinstance(x_min, float):
            x_min = Decimal(str(x_min))
        if isinstance(x_max, float):
            x_max = Decimal(str(x_max))
        if isinstance(y_min, float):
            y_min = Decimal(str(y_min))
        if isinstance(y_max, float):
            y_max = Decimal(str(y_max))
        x_min = x_min.quantize(prec)
        x_max = x_max.quantize(prec)
        y_min = y_min.quantize(prec)
        y_max = y_max.quantize(prec)
        assert x_min <= x_max, f"Negative width: w = {x_max - x_min}"
        assert y_min <= y_max, f"Negative height: h = {y_max - y_min}"
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def width(self) -> Decimal:
        return self.x_max - self.x_min

    def height(self) -> Decimal:
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

    def area(self) -> Decimal:
        return self.width() * self.height()

    def __eq__(self, other):
        return (isinstance(other, Rectangle) and self.x_min == other.x_min and self.x_max == other.x_max
                and self.y_min == other.y_min and self.y_max == other.y_max)

    def __repr__(self):
        # return f"{self.bottomLeft()}, {self.topRight()}"
        return f"topLeft={self.topLeft()}, w={round(self.width(), 4)}, h={round(self.height(), 4)}"

    # allows x_min, x_max, y_min, y_max = rectangle
    def __iter__(self):
        return iter((self.x_min, self.x_max, self.y_min, self.y_max))

    @staticmethod
    def fromCenter(center: Point, w: Decimal, h: Decimal):
        return Rectangle(center.x - w/2, center.x + w/2, center.y - h/2, center.y + h/2)

    @staticmethod
    def fromTopLeft(topLeft: Point, w: Decimal, h: Decimal):
        return Rectangle(topLeft.x, topLeft.x + w, topLeft.y - h, topLeft.y)

    def isPointInRectangle(self, x: Decimal | float, y: Decimal | float) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def containsRectangle(self, r) -> bool:
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

    def plotBorder(self, color: str, alpha: float = 0.5, zorder: int = 3) -> None:
        # TODO: compare the time with the patches version
        plt.plot([self.x_min] * 2, [self.y_min, self.y_max], color, alpha=alpha, zorder=zorder)
        plt.plot([self.x_max] * 2, [self.y_min, self.y_max], color, alpha=alpha, zorder=zorder)
        plt.plot([self.x_min, self.x_max], [self.y_max] * 2, color, alpha=alpha, zorder=zorder)
        plt.plot([self.x_min, self.x_max], [self.y_min] * 2, color, alpha=alpha, zorder=zorder)

    def plotFilled(self, color: str, zorder: int) -> None:
        plt.fill([self.x_min, self.x_min, self.x_max, self.x_max],
                 [self.y_min, self.y_max, self.y_max, self.y_min], color, zorder=zorder)