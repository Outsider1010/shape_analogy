from abc import ABC, abstractmethod

from src.biframemethod.rectangle import Rectangle
from src.shapes.pixelShape import PixelShape


class InnerFrameFinder(ABC):
    """
    Interface for different ways to find an inner frame of a shape
    """

    @abstractmethod
    def findInnerFramePixels(self, shape: PixelShape) -> Rectangle:
        pass
