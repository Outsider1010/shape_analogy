from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Point:
    x: Decimal | float
    y: Decimal | float

    def toCoordSys(self, srcCoordSys, dstCoordSys):
        """
        Assuming this point (`self`) is to be considered inside `srcCoordSys` return the point in the same position as
        `self` but inside `dstCoordSys`.
        So for example with :

        `self`: (2, 3),

        `srcCoordSys`: bottomLeft = (0, 0), w = 5, h = 5

        `dstCoordSys`: bottomLeft = (3, 3), w = 10, h = 10

        we return (7, 9).

        If `srcCoordSys` is `None` or `dstCoordSys` we consider the coordinate systems to be the plan so we return the same point.
        :param srcCoordSys: A rectangle containing this point or None
        :param dstCoordSys: A rectangle containing the resulting point or None
        :return:
        """
        if srcCoordSys is None or dstCoordSys is None:
            return self
        else:
            w = srcCoordSys.width()
            h = srcCoordSys.height()
            w2 = dstCoordSys.width()
            h2 = dstCoordSys.height()
            return Point(dstCoordSys.x_min + w2 * (self.x - srcCoordSys.x_min) / w,
                         dstCoordSys.y_min + h2 * (self.y - srcCoordSys.y_min) / h)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))