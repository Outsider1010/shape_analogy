from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from src.birectangle.cuttingmethod.CuttingMethod import CuttingMethod
from src.shapes.pixelShape import PixelShape


class FirstCuttingIn4Method(CuttingMethod):
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
        big_r = biRectangle.outerRectangle
        little_r = biRectangle.innerRectangle
        return [Rectangle(big_r.x_min, little_r.x_min, little_r.y_min, big_r.y_max),
                Rectangle(little_r.x_min, big_r.x_max, little_r.y_max, big_r.y_max),
                Rectangle(big_r.x_min, little_r.x_max, big_r.y_min, little_r.y_min),
                Rectangle(little_r.x_max, big_r.x_max, big_r.y_min, little_r.y_max)]

    def cutPixels(self, pixelShape: PixelShape, biRectangle: BiRectangle) -> list[PixelShape]:
        return [pixelShape.fromShape(r) for r in self.cutBiRectangle(biRectangle)]