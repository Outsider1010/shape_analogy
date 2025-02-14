from abc import ABC, abstractmethod

from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.rectangle import Rectangle
# DO NOT IMPORT STRATEGIES

class Shape(ABC):

    @abstractmethod
    def getInnerRectangle(self, strategy) -> Rectangle:
        pass

    @abstractmethod
    def getOuterRectangle(self) -> Rectangle:
        pass

    @abstractmethod
    def cut(self, birectangle: BiRectangle, strategy):
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        pass




