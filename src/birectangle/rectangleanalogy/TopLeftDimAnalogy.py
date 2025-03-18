from src.birectangle.rectangleanalogy.RectangleAnalogy import RectangleAnalogy
from src.birectangle.pointanalogy.ArithmeticPointAnalogy import ArithmeticPointAnalogy
from src.birectangle.Rectangle import Rectangle

class TopLeftDimAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        topLeft_a = FA.topLeft()
        topLeft_b = FB.topLeft()
        topLeft_c = FC.topLeft()
        topLeft_d = ArithmeticPointAnalogy().analogy(topLeft_a, topLeft_b, topLeft_c)
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromTopLeft(topLeft_d, w_d, h_d)