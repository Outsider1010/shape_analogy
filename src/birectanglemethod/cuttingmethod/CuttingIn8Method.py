from src.birectanglemethod.birectangle import BiRectangle
from src.birectanglemethod.cuttingmethod.CuttingMethod import CuttingMethod
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

    def cutPixels(self, pixelShape: PixelShape, biRectangle: BiRectangle) -> list[PixelShape]:
        big_r = biRectangle.outerRectangle
        little_r = biRectangle.innerRectangle
        new_shapes = [pixelShape.fromShape(big_r.x_min, little_r.x_min, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(little_r.x_min, little_r.x_max, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, little_r.y_max, big_r.y_max),
                      pixelShape.fromShape(big_r.x_min, little_r.x_min, little_r.y_min, little_r.y_max),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, little_r.y_min, little_r.y_max),
                      pixelShape.fromShape(big_r.x_min, little_r.x_min, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(little_r.x_min, little_r.x_max, big_r.y_min, little_r.y_min),
                      pixelShape.fromShape(little_r.x_max, big_r.x_max, big_r.y_min, little_r.y_min)]
        return new_shapes