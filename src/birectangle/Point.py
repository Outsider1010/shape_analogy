from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Point:
    x: Decimal
    y: Decimal

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))