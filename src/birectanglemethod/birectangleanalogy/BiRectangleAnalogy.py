from abc import ABC, abstractmethod

from src.birectanglemethod.birectangle import BiRectangle


class BiRectangleAnalogy(ABC):
    """
    Interface for different strategies of bi-rectangle analogies
    """

    @abstractmethod
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        pass