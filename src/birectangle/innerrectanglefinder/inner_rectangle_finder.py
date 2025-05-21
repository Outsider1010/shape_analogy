from abc import ABC, abstractmethod

from src.birectangle.rectangle import Rectangle
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles


class InnerRectangleFinder(ABC):
    """
    Interface for different ways to find an inner (axis-aligned) rectangle of a shape
    """

    @abstractmethod
    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        raise NotImplementedError
