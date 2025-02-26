from dataclasses import dataclass
from src.birectangle.Point import Point

import numpy as np

@dataclass(frozen=True)
class Segment:
    A: Point
    B: Point

    def __repr__(self):
        return f"({self.A}, {self.A.y})"