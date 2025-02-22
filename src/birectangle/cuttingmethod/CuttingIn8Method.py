import matplotlib.pyplot as plt

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from src.birectangle.cuttingmethod.CuttingMethod import CuttingMethod
from src.shapes.pixelShape import PixelShape


class CuttingIn8Method(CuttingMethod):
    """
    # #################
    # #     |   |     #
    # #  1  | 2 |  3  #
    # #-----#####-----#
    # #  4  #   #  5  #
    # #-----#####-----#
    # #  6  | 7 |  8  #
    # #     |   |     #
    # #################
    """
    def nbSubShapes(self) -> int:
        return 8

    def cutBiRectangle(self, biRectangle: BiRectangle) -> list[Rectangle]:
        innerR, outerR = biRectangle
        return [Rectangle(outerR.x_min, innerR.x_min, innerR.y_max, outerR.y_max),
                Rectangle(innerR.x_min, innerR.x_max, innerR.y_max, outerR.y_max),
                Rectangle(innerR.x_max, outerR.x_max, innerR.y_max, outerR.y_max),
                Rectangle(outerR.x_min, innerR.x_min, innerR.y_min, innerR.y_max),
                Rectangle(innerR.x_max, outerR.x_max, innerR.y_min, innerR.y_max),
                Rectangle(outerR.x_min, innerR.x_min, outerR.y_min, innerR.y_min),
                Rectangle(innerR.x_min, innerR.x_max, outerR.y_min, innerR.y_min),
                Rectangle(innerR.x_max, outerR.x_max, outerR.y_min, innerR.y_min)]

    def cutPixels(self, pixelShape: PixelShape, biRectangle: BiRectangle) -> list[PixelShape]:
        return [pixelShape.fromShape(r) for r in self.cutBiRectangle(biRectangle)]

    def plotCuttingLines(self, biRectangle: BiRectangle):
        innerR, outerR = biRectangle
        plt.plot([outerR.x_min, innerR.x_min], [innerR.y_max] * 2, "g", linestyle="--")
        plt.plot([outerR.x_min, innerR.x_min], [innerR.y_min] * 2, "g", linestyle="--")
        plt.plot([innerR.x_max, outerR.x_max], [innerR.y_min] * 2, "g", linestyle="--")
        plt.plot([innerR.x_max, outerR.x_max], [innerR.y_max] * 2, "g", linestyle="--")
        plt.plot([innerR.x_min] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        plt.plot([innerR.x_max] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        plt.plot([innerR.x_min] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")
        plt.plot([innerR.x_max] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")
