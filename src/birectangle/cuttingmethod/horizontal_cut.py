from matplotlib import pyplot as plt

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.cuttingmethod.cutting_method import CuttingMethod

class HorizontalCut(CuttingMethod):
    """
    one of the ways to cut
    # #################
    # #               #
    # #       1       #
    # #-----#####-----#
    # #  2  #   #  3  #
    # #-----#####-----#
    # #       4       #
    # #               #
    # #################
    """

    def nbSubShapes(self) -> int:
        return 4

    def cutBiRectangle(self, biRectangle: BiRectangle) -> list[Rectangle]:
        innerR, outerR = biRectangle
        return [Rectangle(outerR.x_min, outerR.x_max, innerR.y_max, outerR.y_max),
                Rectangle(outerR.x_min, innerR.x_min, innerR.y_min, innerR.y_max),
                Rectangle(innerR.x_max, outerR.x_max, innerR.y_min, innerR.y_max),
                Rectangle(outerR.x_min, outerR.x_max, outerR.y_min, innerR.y_min)]

    def plotCuttingLines(self, ax, biRectangle: BiRectangle) -> None:
        innerR, outerR = biRectangle
        ax.plot([outerR.x_min, innerR.x_min], [innerR.y_max] * 2, "g", linestyle="--")
        ax.plot([outerR.x_min, innerR.x_min], [innerR.y_min] * 2, "g", linestyle="--")
        ax.plot([innerR.x_max, outerR.x_max], [innerR.y_min] * 2, "g", linestyle="--")
        ax.plot([innerR.x_max, outerR.x_max], [innerR.y_max] * 2, "g", linestyle="--")

    def plt_colors(self) -> list[str]:
        return ["#ff007f", "b", "#800000", "#8000ff"]