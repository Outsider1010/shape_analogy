from src.basicanalogies.realnumbers import arithmetic
from src.birectangle.point import Point
from src.birectangle.rectangleanalogy.rectangle_analogy import RectangleAnalogy
from src.birectangle.rectangle import Rectangle

class TopLeftDimAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        topLeft_a = FA.topLeft()
        topLeft_b = FB.topLeft()
        topLeft_c = FC.topLeft()
        topLeft_d = Point(arithmetic(topLeft_a.x, topLeft_b.x, topLeft_c.x), arithmetic(topLeft_a.y, topLeft_b.y, topLeft_c.y))
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromTopLeft(topLeft_d, w_d, h_d)