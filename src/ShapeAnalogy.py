from abc import ABC
from src.shapes.shape import Shape

class ShapeAnalogy(ABC):

    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> Shape:
        pass