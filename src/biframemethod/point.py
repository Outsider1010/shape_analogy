from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Point:
    x: float | np.float32
    y: float | np.float32

    def __repr__(self):
        return f"({self.x}, {self.y})"