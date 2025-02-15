from abc import ABC, abstractmethod

from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.rectangle import Rectangle
# DO NOT IMPORT STRATEGIES

class Shape(ABC):
    """
    Interface for different shape representations
    """
    @abstractmethod
    def getInnerFrame(self, strategy) -> Rectangle:
        """
        Find an interior axis-aligned rectangle (= frame) of the shape
        :param strategy: The method used to find the frame
        :return: A frame of the shape
        """
        pass

    @abstractmethod
    def getOuterFrame(self) -> Rectangle:
        """
        Find the axis-aligned minimum bounding box of the shape
        :return: the AABB minimizing area
        """
        pass

    @abstractmethod
    def cut(self, birectangle: BiRectangle, strategy):
        """
        Cut the space between the inner and outer frame of `birectangle` into frames
        and return the subshapes inside each frame
        :param birectangle: The birectangle
        :param strategy: The strategy used to cut
        :return: The list of subshapes
        """
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        """
        Check if the shape doesn't have any point.
        :return: True if the shape doesn't have any point
        """
        pass

    @abstractmethod
    def toSinogram(self, maxAngle: float):
        """
        Create a sinogram of the shape
        :param maxAngle:
        :return: a sinogram (2D array of positive numbers) of the shape
        """
        pass




