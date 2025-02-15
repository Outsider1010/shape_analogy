from abc import ABC, abstractmethod

from src.biframemethod.rectangle import Rectangle


class FrameAnalogy(ABC):
    """
    Interface for different frame analogies
    """

    @abstractmethod
    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        pass