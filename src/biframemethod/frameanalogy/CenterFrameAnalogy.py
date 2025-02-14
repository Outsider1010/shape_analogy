from src.biframemethod.frameanalogy.FrameAnalogy import FrameAnalogy
from src.biframemethod.pointanalogy.ArithmeticPointAnalogy import ArithmeticPointAnalogy
from src.biframemethod.rectangle import Rectangle
from src.point import Point


class CenterFrameAnalogy(FrameAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        center_a = FA.center()
        center_b = FB.center()
        center_c = FC.center()
        center_d = ArithmeticPointAnalogy().analogy(center_a, center_b, center_c)
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromTopLeft(center_d, w_d, h_d)