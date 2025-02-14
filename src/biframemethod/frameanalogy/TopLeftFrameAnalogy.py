from src.biframemethod.frameanalogy.FrameAnalogy import FrameAnalogy
from src.biframemethod.rectangle import Rectangle
from src.biframemethod.point import Point


class TopLeftFrameAnalogy(FrameAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        topLeft_a = FA.topLeft()
        topLeft_b = FB.topLeft()
        topLeft_c = FC.topLeft()
        topLeft_d = Point.analogy(topLeft_a, topLeft_b, topLeft_c)
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromTopLeft(topLeft_d, w_d, h_d)