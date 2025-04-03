from matplotlib import pyplot as plt

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.cuttingmethod.cutting_method import CuttingMethod

class CutIn4EqualParts1(CuttingMethod):
    """
    one of the ways to cut
    # #################
    # #     |         #
    # #  1  |    2    #
    # #     #####-----#
    # #     #   #     #
    # #-----#####     #
    # #    3    |  4  #
    # #         |     #
    # #################
    """
    def nbSubShapes(self) -> int:
        return 4

    def cutBiRectangle(self, biRectangle: BiRectangle) -> list[Rectangle]:
        innerR, outerR = biRectangle
        return [Rectangle(outerR.x_min, innerR.x_min, innerR.y_min, outerR.y_max),
                Rectangle(innerR.x_min, outerR.x_max, innerR.y_max, outerR.y_max),
                Rectangle(outerR.x_min, innerR.x_max, outerR.y_min, innerR.y_min),
                Rectangle(innerR.x_max, outerR.x_max, outerR.y_min, innerR.y_max)]

    def plotCuttingLines(self, biRectangle: BiRectangle) -> None:
        innerR, outerR = biRectangle
        plt.plot([outerR.x_min, innerR.x_min], [innerR.y_min] * 2, "g", linestyle="dotted")
        plt.plot([innerR.x_max, outerR.x_max], [innerR.y_max] * 2, "g", linestyle="dotted")
        plt.plot([innerR.x_min] * 2, [innerR.y_max, outerR.y_max], "g", linestyle="dotted")
        plt.plot([innerR.x_max] * 2, [outerR.y_min, innerR.y_min], "g", linestyle="dotted")

    def plt_colors(self) -> list[str]:
        return ["#ff007f", "b", "#800000", "#8000ff"]