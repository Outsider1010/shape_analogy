from abc import ABC, abstractmethod

from src.biframemethod.birectangle import BiRectangle
from src.shapes.pixelShape import PixelShape


class CuttingMethod(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def cutPixels(self, pixelShape: PixelShape, biFrame: BiRectangle) -> list[PixelShape]:
        pass

    @abstractmethod
    def nbSubShapes(self) -> int:
        pass