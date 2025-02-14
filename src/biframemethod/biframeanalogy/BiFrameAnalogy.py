from abc import ABC, abstractmethod

from src.biframemethod.birectangle import BiRectangle


class BiFrameAnalogy(ABC):
    """
    Interface for different strategies of bi-frame analogies
    """
    def __init__(self):
        pass

    @abstractmethod
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        pass