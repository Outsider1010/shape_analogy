import largestinteriorrectangle as lir

from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point
from src.shapes.pixelShape import PixelShape


class LargestRectangleFinder(InnerRectangleFinder):

    def findInnerRectanglePixels(self, shape: PixelShape) -> Rectangle:
        # find the largest interior rectangle
        topLeft_x, topLeft_y, w, h = lir.lir(shape.pixels)
        w2, h2 = shape.dim()

        # have to adjust because we consider the center of the image to be the origin
        return Rectangle.fromTopLeft(Point(topLeft_x - h2 / 2, w2 / 2 - topLeft_y), w, h)