from decimal import Decimal
from typing import Iterable

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from .shape import Shape
# DO NOT IMPORT STRATEGIES (to avoid circular imports)

class UnionRectangles(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """
    def __init__(self, rects: Iterable[Rectangle] = None):
        if rects is None:
            self.rectangles = []
        else:
            self.rectangles = list(rects)

    def addRectangle(self, r: Rectangle):
        self.rectangles.append(r)

    def __add__(self, other):
        return UnionRectangles(self.rectangles + other.rectangles)

    def __repr__(self):
        return str(self.rectangles)

    def getOuterRectangle(self) -> Rectangle:
        if len(self.rectangles) == 0:
            return Rectangle(0, 0, 0, 0)
        i = iter(self.rectangles)
        r = next(i)
        x_min, x_max,y_min, y_max = r
        r = next(i, None)
        while r:
            x_min = min(x_min, r.x_min)
            x_max = max(x_max, r.x_max)
            y_min = min(y_min, r.y_min)
            y_max = max(y_max, r.y_max)
            r = next(i, None)
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectangleUnionR(self)

    def fromShape(self, frame: Rectangle):
        res = UnionRectangles()
        for r in self.rectangles:
            x = frame.intersection(r)
            if x is not None and x.area() > 0:
                res.addRectangle(x)
        return res

    def equiv(self, fromCoordSysR: Rectangle | None, toCoordSysR: Rectangle | None):
        if fromCoordSysR is None or toCoordSysR is None:
            return self
        else:
            res = UnionRectangles()
            for r in self.rectangles:
                b = BiRectangle(fromCoordSysR, r)
                res.addRectangle(b.innerEquiv(toCoordSysR))
            return res

    def isPointInShape(self, x: Decimal | float, y: Decimal | float) -> bool:
        return any(r.isPointInRectangle(x, y) for r in self.rectangles)

    def __eq__(self, other):
        if not isinstance(other, UnionRectangles):
            return False
        # TODO
        pass

    def isEmpty(self) -> bool:
        return len(self.rectangles) == 0

    def plot(self) -> None:
        for r in self.rectangles:
            r.plotFilled("k", 1)

    def toPixels(self) -> {}:
        # TODO
        pass

    def toImage(self, name: str = "default.bmp"):
        self.toPixels().toImage(name)

    def toSinogram(self, maxAngle: float = 180.):
        # TODO
        pass
