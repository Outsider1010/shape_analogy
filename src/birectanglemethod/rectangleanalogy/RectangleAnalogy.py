from abc import ABC, abstractmethod

from src.birectanglemethod.rectangle import Rectangle


class RectangleAnalogy(ABC):
    """
    Interface for different rectangle analogies
    """

    @abstractmethod
    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        pass