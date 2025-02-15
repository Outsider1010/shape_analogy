from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __repr__(self):
        return f"({self.x}, {self.y})"