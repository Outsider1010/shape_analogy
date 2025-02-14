from abc import ABC, abstractmethod

from src.biframemethod.rectangle import Rectangle
from src.shapes.pixelShape import PixelShape


class InnerFrameFinder(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def findInnerFramePixels(self, shape: PixelShape) -> Rectangle:
        pass
