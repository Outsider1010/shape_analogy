from src.basicanalogies.realnumbers import arithmetic
from src.birectangle.point import Point
from src.birectangle.rectangleanalogy.rectangle_analogy import RectangleAnalogy
from src.birectangle.rectangle import Rectangle


class CenterDimAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        center_a = FA.center()
        center_b = FB.center()
        center_c = FC.center()
        center_d = Point(arithmetic(center_a.x, center_b.x, center_c.x), arithmetic(center_a.y, center_b.y, center_c.y))
        w_d = FC.width() * FB.width() / FA.width()
        h_d = FC.height() * FB.height() / FA.height()
        return Rectangle.fromCenter(center_d, w_d, h_d)