from abc import ABC, abstractmethod

from src.birectangle.Rectangle import Rectangle
from src.shapes.UnionRectangles import UnionRectangles
from src.shapes.pixelShape import PixelShape


class InnerRectangleFinder(ABC):
    """
    Interface for different ways to find an inner (axis-aligned) rectangle of a shape
    """

    @abstractmethod
    def findInnerRectanglePixels(self, shape: PixelShape) -> Rectangle:
        raise NotImplementedError

    @abstractmethod
    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        raise NotImplementedError
