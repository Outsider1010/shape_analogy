from abc import ABC, abstractmethod

from src.birectangle.Rectangle import Rectangle
from src.shapes.union_rectangles import UnionRectangles


class InnerRectangleFinder(ABC):
    """
    Interface for different ways to find an inner (axis-aligned) rectangle of a shape
    """

    @abstractmethod
    def findInnerRectanglePixels(self, shape) -> Rectangle:
        raise NotImplementedError

    @abstractmethod
    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        raise NotImplementedError
