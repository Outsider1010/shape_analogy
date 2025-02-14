import largestinteriorrectangle as lir

from src.biframemethod.innerframefinder.InnerFrameFinder import InnerFrameFinder
from src.biframemethod.rectangle import Rectangle
from src.point import Point
from src.shapes.pixelShape import PixelShape


class LargestFrameFinder(InnerFrameFinder):

    def findInnerFramePixels(self, shape: PixelShape) -> Rectangle:
        # find the largest interior rectangle
        topLeft_x, topLeft_y, w, h = lir.lir(shape.pixels)
        w2, h2 = shape.dim()

        # have to adjust because we consider the center of the image to be the origin
        return Rectangle.fromTopLeft(Point(topLeft_x - h2 / 2, w2 / 2 - topLeft_y), w, h)