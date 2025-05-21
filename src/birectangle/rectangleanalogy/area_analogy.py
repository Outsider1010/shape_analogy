
from src.basicanalogies.realnumbers import geometric
from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.rectangle_analogy import RectangleAnalogy

class AreaAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        x_a, y_a = FA.center()
        x_b, y_b = FB.center()
        x_c, y_c = FC.center()

        w_a, h_a = FA.width(), FA.height()
        w_b, h_b = FB.width(), FB.height()
        w_c, h_c = FC.width(), FC.height()

        w_d = geometric(w_a, w_b, w_c)
        h_d = geometric(h_a, h_b, h_c)
        area_d = w_d * h_d
        x_d = area_d * geometric(x_a / FA.area(), x_b / FB.area(), x_c / FC.area())
        y_d = area_d * geometric(y_a / FA.area(), y_b / FB.area(), y_c / FC.area())

        return Rectangle.fromCenter(Point(x_d, y_d), w_d, h_d)