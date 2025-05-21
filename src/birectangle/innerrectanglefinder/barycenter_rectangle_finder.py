import numpy as np

from src.birectangle.innerrectanglefinder.inner_rectangle_finder import *
from src.birectangle.point import Point
from src.birectangle.Segment import Segment


def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)


class BarycenterRectangleFinder(InnerRectangleFinder):

    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        """
        Retourne le plus grand rectangle intérieur contenant le barycentre (ou un point ajusté).
        Contrairement à la version précédente, le barycentre n'est pas forcément le centre du rectangle,
        mais doit absolument rester inclus dans celui-ci.

        Chaque côté du rectangle est étendu indépendamment (asymétriquement), tant que :
            - Le rectangle reste dans la forme.
            - Le barycentre reste inclus.
        """

        # Étape 1 : Calcul du barycentre pondéré.
        total_area = 0
        sum_x = 0
        sum_y = 0
        for r in shape.rectangles:
            width = r.x_max - r.x_min
            height = r.y_max - r.y_min
            area = width * height
            center = r.center()
            total_area += area
            sum_x += center.x * area
            sum_y += center.y * area
        if total_area > 0:
            Cx = sum_x / total_area
            Cy = sum_y / total_area
        else:
            Cx = 0
            Cy = 0
        P = Point(Cx, Cy)

        # Ajustement si le barycentre n’est pas dans la forme.
        if not shape.isPointInShape(P.x, P.y):
            min_dist = None
            nearest = None
            for r in shape.rectangles:
                pt = r.center()
                dist_sq = (pt.x - P.x) ** 2 + (pt.y - P.y) ** 2
                if min_dist is None or dist_sq < min_dist:
                    min_dist = dist_sq
                    nearest = pt
            P = nearest

        # Étape 2 : Initialisation.
        left = right = P.x
        top = bottom = P.y

        initial_step = 0.1
        tolerance = 0.001

        def can_expand_left(x, bottom, top, step):
            new_left = x - step
            seg = Segment(Point(new_left, bottom), Point(new_left, top))
            return shape.isVerticalSegmentInShape(seg) and new_left <= P.x

        def can_expand_right(x, bottom, top, step):
            new_right = x + step
            seg = Segment(Point(new_right, bottom), Point(new_right, top))
            return shape.isVerticalSegmentInShape(seg) and new_right >= P.x

        def can_expand_top(y, left, right, step):
            new_top = y + step
            seg = Segment(Point(left, new_top), Point(right, new_top))
            return shape.isHorizontalSegmentInShape(seg) and new_top >= P.y

        def can_expand_bottom(y, left, right, step):
            new_bottom = y - step
            seg = Segment(Point(left, new_bottom), Point(right, new_bottom))
            return shape.isHorizontalSegmentInShape(seg) and new_bottom <= P.y

        # Étape 3 : Extension asymétrique autour du barycentre.
        for direction in ['left', 'right', 'top', 'bottom']:
            step = initial_step
            while step > tolerance:
                if direction == 'left' and can_expand_left(left, bottom, top, step):
                    left -= step
                elif direction == 'right' and can_expand_right(right, bottom, top, step):
                    right += step
                elif direction == 'top' and can_expand_top(top, left, right, step):
                    top += step
                elif direction == 'bottom' and can_expand_bottom(bottom, left, right, step):
                    bottom -= step
                else:
                    step /= 2

        # Étape 4 : Construction du rectangle final.
        width = right - left
        height = top - bottom
        result = Rectangle.fromTopLeft(Point(left, top), width, height)
        return result



