from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.cuttingmethod.CuttingMethod import CuttingMethod
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

    def cutPixels(self, pixelShape: PixelShape, biFrame: BiRectangle) -> list[PixelShape]:
        big_r = biFrame.outerRectangle
        little_r = biFrame.innerRectangle
        new_shapes = [pixelShape.fromShape(big_r.x_min, little_r.x_min, big_r.y_min, little_r.y_max),
                      pixelShape.fromShape(little_r.x_min, big_r.x_max, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(big_r.x_min, little_r.x_max, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, little_r.y_min, big_r.y_max)]
        return new_shapes