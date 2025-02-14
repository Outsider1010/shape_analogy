from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.cuttingmethod.CuttingMethod import CuttingMethod
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

    def cutPixels(self, pixelShape: PixelShape, biFrame: BiRectangle) -> list[PixelShape]:
        big_r = biFrame.outerRectangle
        little_r = biFrame.innerRectangle
        new_shapes = [pixelShape.fromShape(big_r.x_min, little_r.x_min, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(little_r.x_min, little_r.x_max, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(big_r.x_min, little_r.x_min, little_r.y_min, little_r.y_max),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, little_r.y_min, little_r.y_max),
                      pixelShape.fromShape(big_r.x_min, little_r.x_min, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(little_r.x_min, little_r.x_max, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, little_r.y_max, big_r.y_max)]
        return new_shapes