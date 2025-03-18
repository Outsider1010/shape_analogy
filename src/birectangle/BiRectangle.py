from decimal import Decimal
from typing import Iterator

import numpy as np

from src.birectangle.Point import Point
from src.birectangle.Rectangle import Rectangle

class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(
            innerRectangle), (f"Inner rectangle should be contained by outer rectangle.\n"
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

    def reduceInnerTo(self, r_x_min: Decimal, r_x_max: Decimal, r_y_min: Decimal, r_y_max: Decimal) -> None:
        _, outerR = self
        cx, w = np.linalg.solve(np.array([[2 * float(r_x_min), -1], [2 * float(r_x_max), 1]]),
                                np.array([2 * float(r_x_min * outerR.x_min), 2 * float(r_x_max * outerR.x_max)]))

        cy, h = np.linalg.solve(np.array([[2 * float(r_y_min), -1], [2 * float(r_y_max), 1]]),
                                np.array([2 * float(r_y_min * outerR.y_min), 2 * float(r_y_max * outerR.y_max)]))

        r = Rectangle.fromCenter(Point(cx, cy), w, h)
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

        return Rectangle(toCoordSysR.x_min + x_min_rescale * w, toCoordSysR.x_min + x_max_rescale * w,
                         toCoordSysR.y_min + y_min_rescale * w, toCoordSysR.y_min + y_max_rescale * w)