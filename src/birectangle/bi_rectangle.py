from decimal import Decimal
from typing import Iterator

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