from abc import ABC, abstractmethod

from src.birectangle.rectangle import Rectangle
# DO NOT IMPORT STRATEGIES

class Shape(ABC):
    """
    Interface for different shape representations
    """
    @abstractmethod
    def getInnerRectangle(self, strategy) -> Rectangle:
        """
        Find an interior axis-aligned rectangle of the shape
        :param strategy: The method used to find the rectangle
        :return: A (axis-aligned) rectangle of the shape
        """
        raise NotImplementedError

    @abstractmethod
    def outer_rectangle(self) -> Rectangle:
        """
        Find the axis-aligned minimum bounding box of the shape
        :return: the AABB minimizing area
        """
        raise NotImplementedError

    @abstractmethod
    def fromShape(self, r: Rectangle):
        raise NotImplementedError

    @abstractmethod
    def equiv(self, fromCoordSysR: Rectangle, toCoordSysR: Rectangle):
        raise NotImplementedError

    @abstractmethod
    def isEmpty(self) -> bool:
        """
        Check if the shape doesn't have any point.
        :return: True if the shape doesn't have any point
        """
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        """
        Plot the shape with matplotlib
        :return: Nothing
        """
        pass

    @abstractmethod
    def toImage(self, name='default.bmp'):
        pass

    @abstractmethod
    def toSinogram(self, maxAngle: float):
        """
        Create a sinogram of the shape
        :param maxAngle:
        :return: a sinogram (2D array of positive numbers) of the shape
        """
        raise NotImplementedError




