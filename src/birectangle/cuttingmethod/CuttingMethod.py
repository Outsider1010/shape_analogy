from abc import ABC, abstractmethod

from src.birectangle.BiRectangle import BiRectangle
from src.shapes.pixelShape import PixelShape


class CuttingMethod(ABC):
    """
    Interface for different cutting strategies
    """

    @abstractmethod
    def cutPixels(self, pixelShape: PixelShape, biRectangle: BiRectangle) -> list[PixelShape]:
        pass

    @abstractmethod
    def nbSubShapes(self) -> int:
        pass