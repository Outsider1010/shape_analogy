import matplotlib.pyplot as plt

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.cuttingmethod.cutting_method import CuttingMethod


class CuttingIn8(CuttingMethod):
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

    def plotCuttingLines(self, ax, biRectangle: BiRectangle):
        innerR, outerR = biRectangle
        ax.plot([outerR.x_min, innerR.x_min], [innerR.y_max] * 2, "g", linestyle="--")
        ax.plot([outerR.x_min, innerR.x_min], [innerR.y_min] * 2, "g", linestyle="--")
        ax.plot([innerR.x_max, outerR.x_max], [innerR.y_min] * 2, "g", linestyle="--")
        ax.plot([innerR.x_max, outerR.x_max], [innerR.y_max] * 2, "g", linestyle="--")
        ax.plot([innerR.x_min] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        ax.plot([innerR.x_max] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        ax.plot([innerR.x_min] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")
        ax.plot([innerR.x_max] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")
