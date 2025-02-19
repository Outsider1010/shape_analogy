from src.birectanglemethod.rectangleanalogy.RectangleAnalogy import RectangleAnalogy
from src.birectanglemethod.pointanalogy.ArithmeticPointAnalogy import ArithmeticPointAnalogy
from src.birectanglemethod.rectangle import Rectangle


class CenterDimAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        center_a = FA.center()
        center_b = FB.center()
        center_c = FC.center()
        center_d = ArithmeticPointAnalogy().analogy(center_a, center_b, center_c)
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromCenter(center_d, w_d, h_d)