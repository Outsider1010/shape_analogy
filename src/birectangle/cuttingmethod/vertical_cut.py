from matplotlib import pyplot as plt

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.cuttingmethod.cutting_method import CuttingMethod

class VerticalCut(CuttingMethod):
    """
    one of the ways to cut
    # #################
    # #     |   |     #
    # #     | 2 |     #
    # #     #####     #
    # #  1  #   #  4  #
    # #     #####     #
    # #     | 3 |     #
    # #     |   |     #
    # #################
    """

    def nbSubShapes(self) -> int:
        return 4

    def cutBiRectangle(self, biRectangle: BiRectangle) -> list[Rectangle]:
        innerR, outerR = biRectangle
        return [Rectangle(outerR.x_min, innerR.x_min, outerR.y_min, outerR.y_max),
                Rectangle(innerR.x_min, innerR.x_max, innerR.y_max, outerR.y_max),
                Rectangle(innerR.x_min, innerR.x_max, outerR.y_min, innerR.y_min),
                Rectangle(innerR.x_max, outerR.x_max, outerR.y_min, outerR.y_max)]

    def plotCuttingLines(self, ax, biRectangle: BiRectangle):
        innerR, outerR = biRectangle
        ax.plot([innerR.x_min] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        ax.plot([innerR.x_max] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="--")
        ax.plot([innerR.x_min] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")
        ax.plot([innerR.x_max] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="--")

    def plt_colors(self) -> list[str]:
        return ["#ff007f", "b", "#800000", "#8000ff"]