from src.basicanalogies.realnumbers import arithmetic
from src.biframemethod.pointanalogy.PointAnalogy import PointAnalogy
from src.biframemethod.point import Point


class ArithmeticPointAnalogy(PointAnalogy):

    def analogy(self, A: Point, B: Point, C: Point) -> Point:
        return Point(arithmetic(A.x, B.x, C.x), arithmetic(A.y, B.y, C.y))