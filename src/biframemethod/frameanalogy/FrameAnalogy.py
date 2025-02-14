from abc import ABC, abstractmethod

from src.biframemethod.rectangle import Rectangle


class FrameAnalogy(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        pass