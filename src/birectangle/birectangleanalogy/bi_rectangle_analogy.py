from abc import ABC, abstractmethod

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle


class BiRectangleAnalogy(ABC):
    """
    Interface for different strategies of bi-rectangle analogies
    """

    @abstractmethod
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        raise NotImplementedError