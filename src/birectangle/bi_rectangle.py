from decimal import Decimal
from typing import Iterator

import numpy as np
from networkx.algorithms.distance_measures import center

from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        b = outerRectangle.containsRectangle(innerRectangle)
        if not b:
            limit = Decimal('1E-25')
            if not outerRectangle.y_min <= innerRectangle.y_min and outerRectangle.y_min - innerRectangle.y_min < limit:
                innerRectangle.y_min = outerRectangle.y_min
            if not outerRectangle.x_min <= innerRectangle.x_min and outerRectangle.x_min - innerRectangle.x_min < limit:
                innerRectangle.x_min = outerRectangle.x_min
            if not outerRectangle.y_max >= innerRectangle.y_max and innerRectangle.y_max - outerRectangle.y_max < limit:
                innerRectangle.y_max = outerRectangle.y_max
            if not outerRectangle.x_max >= innerRectangle.x_max and innerRectangle.x_max - outerRectangle.x_max < limit:
                innerRectangle.x_max = outerRectangle.x_max
        assert outerRectangle.containsRectangle(innerRectangle), (f"Inner rectangle should be contained by outer rectangle.\n"
                              f"Outer : {outerRectangle}\nInner : {innerRectangle}")

        self.innerRectangle: Rectangle = innerRectangle
        self.outerRectangle: Rectangle = outerRectangle

    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + " / Inner: " + str(self.innerRectangle)

    def __iter__(self) -> Iterator[Rectangle]:
        return iter((self.innerRectangle, self.outerRectangle))

    def separate(self, epsilon: Decimal) -> None:
        if epsilon != 0:
            innerR, outerR = self
            w, h = innerR.width(), innerR.height()
            self.innerRectangle = Rectangle(innerR.x_min + epsilon * (innerR.x_min == outerR.x_min) * w,
                                            innerR.x_max - epsilon * (innerR.x_max == outerR.x_max) * w,
                                            innerR.y_min + epsilon * (innerR.y_min == outerR.y_min) * h,
                                            innerR.y_max - epsilon * (innerR.y_max == outerR.y_max) * h)

    def center_x_min_ratio(self) -> Decimal:
        return self.innerRectangle.width() / (2 * (self.innerRectangle.center().x - self.outerRectangle.x_min))

    def center_x_max_ratio(self) -> Decimal:
        return self.innerRectangle.width() / (2 * (self.outerRectangle.x_max - self.innerRectangle.center().x))

    def center_y_min_ratio(self) -> Decimal:
        return self.innerRectangle.height() / (2 * (self.innerRectangle.center().y - self.outerRectangle.y_min))

    def center_y_max_ratio(self) -> Decimal:
        return self.innerRectangle.height() / (2 * (self.outerRectangle.y_max - self.innerRectangle.center().y))

    def center_xy_ratios(self):
        return self.center_x_min_ratio(), self.center_x_max_ratio(), self.center_y_min_ratio(), self.center_y_max_ratio()

    def reduceInnerTo(self, r_x_min: Decimal, r_x_max: Decimal, r_y_min: Decimal, r_y_max: Decimal) -> None:
        _, outerR = self
        cx, w = np.linalg.solve(np.array([[2 * float(r_x_min), -1], [2 * float(r_x_max), 1]]),
                                np.array([2 * float(r_x_min * outerR.x_min), 2 * float(r_x_max * outerR.x_max)]))

        cy, h = np.linalg.solve(np.array([[2 * float(r_y_min), -1], [2 * float(r_y_max), 1]]),
                                np.array([2 * float(r_y_min * outerR.y_min), 2 * float(r_y_max * outerR.y_max)]))

        r = Rectangle.fromCenter(Point(cx, cy), w, h)
        b = outerR.containsRectangle(r)
        if not b:
            limit = Decimal('1E-25')
            if not outerR.y_min <= r.y_min and outerR.y_min - r.y_min < limit:
                r.y_min = outerR.y_min
            if not outerR.x_min <= r.x_min and outerR.x_min - r.x_min < limit:
                r.x_min = outerR.x_min
            if not outerR.y_max >= r.y_max and r.y_max - outerR.y_max < limit:
                r.y_max = outerR.y_max
            if not outerR.x_max >= r.x_max and r.x_max - outerR.x_max < limit:
                r.x_max = outerR.x_max
        assert outerR.containsRectangle(r), (f"Inner rectangle should be contained by outer rectangle after ratio.\n"
                              f"Outer : {outerR}\nInner : {r}")
        self.innerRectangle = r

    def innerEquiv(self, toCoordSysR: Rectangle) -> Rectangle:
        w = self.outerRectangle.width()
        h = self.outerRectangle.height()
        x_min_rescale = (self.innerRectangle.x_min - self.outerRectangle.x_min) / w
        x_max_rescale = (self.innerRectangle.x_max - self.outerRectangle.x_min) / w
        y_min_rescale = (self.innerRectangle.y_min - self.outerRectangle.y_min) / h
        y_max_rescale = (self.innerRectangle.y_max - self.outerRectangle.y_min) / h

        w2 = toCoordSysR.width()
        h2 = toCoordSysR.height()
        return Rectangle(toCoordSysR.x_min + x_min_rescale * w2, toCoordSysR.x_min + x_max_rescale * w2,
                         toCoordSysR.y_min + y_min_rescale * h2, toCoordSysR.y_min + y_max_rescale * h2)