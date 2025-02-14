from dataclasses import dataclass
from . basicanalogies.realnumbers import arithmetic

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    @staticmethod
    def analogy(A, B, C):
        return Point(arithmetic(A.x, B.x, C.x), arithmetic(A.y, B.y, C.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"