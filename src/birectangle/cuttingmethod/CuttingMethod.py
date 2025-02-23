from abc import ABC, abstractmethod

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from src.shapes.pixelShape import PixelShape


class CuttingMethod(ABC):
    """
    Interface for different cutting strategies
    """
    @abstractmethod
    def cutBiRectangle(self, biRectangle: BiRectangle) -> list[Rectangle]:
        """
        Return the different rectangles obtained by cutting up the area of the outer rectangle
        not contained in the inner rectangle of `biRectangle`
        :param biRectangle: a bi-rectangle, i.e. a couple of rectangles (one containing the other)
        :return: a list of rectangles
        """
        pass

    @abstractmethod
    def cutPixels(self, pixelShape: PixelShape, biRectangle: BiRectangle) -> list[PixelShape]:
        """
        Return the different part of the shape `pixelShape` contained inside each rectangle obtained by cutting
        up the area between the outer and inner rectangles of the bi-rectangle.
        :param pixelShape: The shape
        :param biRectangle: The bi-rectangle
        :return: a list of subshapes of `pixelShape`
        """
        pass

    @abstractmethod
    def plotCuttingLines(self, biRectangle: BiRectangle) -> None:
        """
        Draw the cutting lines between the rectangles in a plot
        :param biRectangle: the bi-rectangle being cut
        :return: Nothing.
        """
        pass

    @abstractmethod
    def nbSubShapes(self) -> int:
        """
        :return: The number of rectangles obtained after cutting
        """
        pass