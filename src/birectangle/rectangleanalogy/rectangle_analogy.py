from abc import ABC, abstractmethod

from src.birectangle.rectangle import Rectangle


class RectangleAnalogy(ABC):
    """
    Interface for different rectangle analogies
    """

    @abstractmethod
    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        raise NotImplementedError