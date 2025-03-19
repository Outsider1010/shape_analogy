from decimal import Decimal

from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.rectangle_analogy import RectangleAnalogy

# DOESN'T VERIFY "ECHANGE DE MOYENS"
class CoordAnalogy(RectangleAnalogy):

    def analogy(self, FA: Rectangle, FB: Rectangle, FC: Rectangle) -> Rectangle:
        x, y = FA.center()
        x_c, y_c = FC.center()
        two = Decimal(2)
        mi_w_c = FC.width() / two
        mi_h_c = FC.height() / two
        r_x_min = (FA.width() / two) / (x - FB.x_min)
        r_x_max = (FA.width() / two) / (FB.x_max - x)

        r_y_min = (FA.height() / two) / (y - FB.y_min)
        r_y_max = (FA.height() / two) / (FB.y_max - y)

        x_min_d = (r_x_min * x_c - mi_w_c) / r_x_min
        x_max_d = (r_x_max * x_c + mi_w_c) / r_x_max
        y_min_d = (r_y_min * y_c - mi_h_c) / r_y_min
        y_max_d = (r_y_max * y_c + mi_h_c) / r_y_max

        return Rectangle(x_min_d, x_max_d, y_min_d, y_max_d)