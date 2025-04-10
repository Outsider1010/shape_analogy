from decimal import Decimal
import numpy as np

from src.birectangle.innerrectanglefinder.inner_rectangle_finder import *
from src.birectangle.point import Point
from src.birectangle.Segment import Segment
from decimal import Decimal
from math import floor, ceil


def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)


class BarycenterRectangleFinder(InnerRectangleFinder):

    def findInnerRectanglePixels(self, shape) -> Rectangle:
        """
        Recherche du rectangle intérieur à partir des pixels de la forme.
        La méthode part du barycentre (ou d’un pixel ajusté si le barycentre est extérieur)
        et étend le rectangle initial (réduit à un point P) le long de la diagonale de pente -1.
        Si l'extension simultanée des coins H (haut-gauche) et B (bas-droite) n'est pas possible,
        le coin H est favorisé (extension asymétrique).
        """
        matrix = shape.pixels
        h, w = shape.dim()

        # Pré-calcul des demi-dimensions en Decimal
        half_h = Decimal(h) / Decimal(2)
        half_w = Decimal(w) / Decimal(2)
        dec_half = Decimal('0.5')

        # =================================================
        #               Calcul du barycentre
        # =================================================
        ys_idx, xs_idx = np.where(matrix)
        xs_dec = [Decimal(x) - (Decimal(w) / Decimal(2)) + dec_half for x in xs_idx]
        ys_dec = [half_h - Decimal(y) - dec_half for y in ys_idx]

        if xs_dec and ys_dec:
            sum_x = sum(xs_dec, Decimal(0))
            sum_y = sum(ys_dec, Decimal(0))
            count = Decimal(len(xs_dec))
            center_x = sum_x / count
            center_y = sum_y / count
        else:
            center_x, center_y = Decimal(0), Decimal(0)

        center = Point(center_x, center_y)
        Cx, Cy = center.x, center.y

        # Si le centre n'est pas dans la forme, on cherche le pixel le plus proche
        if not shape.isPointInShape(Cx, Cy):
            points = list(zip(xs_dec, ys_dec))

            def sq_distance(p):
                return (p[0] - Cx) ** 2 + (p[1] - Cy) ** 2

            nearest_idx = min(range(len(points)), key=lambda i: sq_distance(points[i]))
            nearestPixel = list(points[nearest_idx])

            dx = Cx - nearestPixel[0]
            dy = Cy - nearestPixel[1]
            dx_positive = dx > 0
            dy_positive = dy > 0
            if abs(dx) >= dec_half:
                nearestPixel[0] += dec_half if dx_positive else -dec_half
            if abs(dy) >= dec_half:
                nearestPixel[1] += dec_half if dy_positive else -dec_half

            center = Point(nearestPixel[0], nearestPixel[1])
            Cx, Cy = center.x, center.y

        print("Center :", center)

        # =================================================
        #             Expansion du rectangle
        # =================================================
        # Initialisation : le rectangle démarre réduit à P (H = B = centre)
        Hx, Hy = Cx, Cy  # Coin supérieur gauche (top-left)
        Bx, By = Cx, Cy  # Coin inférieur droit (bottom-right)

        initial_step = Decimal('0.1')
        step = initial_step
        tolerance = Decimal('0.001')

        # --- Fonctions d'aide pour tester l'extension ---

        def can_expand_simultaneously(Hx, Hy, Bx, By, step):
            # Extension simultanée de H et B
            new_Hx = Hx - step
            new_Hy = Hy + step
            new_Bx = Bx + step
            new_By = By - step

            # Vérification des coins
            if not (shape.isPointInShape(new_Hx, new_Hy) and shape.isPointInShape(new_Bx, new_By)):
                return False

            # Vérification des segments horizontaux (haut et bas)
            top_seg = Segment(Point(new_Hx, new_Hy), Point(new_Bx, new_Hy))
            bottom_seg = Segment(Point(new_Hx, new_By), Point(new_Bx, new_By))
            if not (shape.isHorizontalSegmentInShape(top_seg) and shape.isHorizontalSegmentInShape(bottom_seg)):
                return False

            # Vérification des segments verticaux (gauche et droite)
            left_seg = Segment(Point(new_Hx, new_By), Point(new_Hx, new_Hy))
            right_seg = Segment(Point(new_Bx, new_By), Point(new_Bx, new_Hy))
            if not (shape.isVerticalSegmentInShape(left_seg) and shape.isVerticalSegmentInShape(right_seg)):
                return False

            return True

        def can_expand_H(Hx, Hy, Bx, By, step):
            # Extension asymétrique : déplacement seul du coin H (haut-gauche)
            new_Hx = Hx - step
            new_Hy = Hy + step

            if not shape.isPointInShape(new_Hx, new_Hy):
                return False
            # Vérifier la validité du segment horizontal supérieur (de H à B en x)
            top_seg = Segment(Point(new_Hx, new_Hy), Point(Bx, new_Hy))
            if not shape.isHorizontalSegmentInShape(top_seg):
                return False
            # Vérifier la validité du segment vertical gauche (de H en y jusqu'à le bas actuel)
            left_seg = Segment(Point(new_Hx, By), Point(new_Hx, new_Hy))
            if not shape.isVerticalSegmentInShape(left_seg):
                return False
            return True

        def can_expand_B(Hx, Hy, Bx, By, step):
            # Extension asymétrique : déplacement seul du coin B (bas-droite)
            new_Bx = Bx + step
            new_By = By - step

            if not shape.isPointInShape(new_Bx, new_By):
                return False
            # Vérifier la validité du segment horizontal inférieur
            bottom_seg = Segment(Point(Hx, new_By), Point(new_Bx, new_By))
            if not shape.isHorizontalSegmentInShape(bottom_seg):
                return False
            # Vérifier la validité du segment vertical droit
            right_seg = Segment(Point(new_Bx, By), Point(new_Bx, new_By))
            if not shape.isVerticalSegmentInShape(right_seg):
                return False
            return True

        # Boucle d'extension avec test d'extension simultanée puis asymétrique
        while step > tolerance:
            if can_expand_simultaneously(Hx, Hy, Bx, By, step):
                Hx -= step
                Hy += step
                Bx += step
                By -= step
            elif can_expand_H(Hx, Hy, Bx, By, step):
                # Extension seulement du coin H (prioritaire)
                Hx -= step
                Hy += step
            elif can_expand_B(Hx, Hy, Bx, By, step):
                # Extension seulement du coin B
                Bx += step
                By -= step
            else:
                step = step / Decimal(2)

        width = Bx - Hx
        height = Hy - By
        rectangle = Rectangle.fromTopLeft(Point(Hx, Hy), width, height)
        return rectangle

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
        total_area = Decimal('0')
        sum_x = Decimal('0')
        sum_y = Decimal('0')
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
            Cx = Decimal('0')
            Cy = Decimal('0')
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
        print("Barycentre retenu :", P)

        # Étape 2 : Initialisation.
        left = right = P.x
        top = bottom = P.y

        initial_step = Decimal('0.1')
        tolerance = Decimal('0.001')

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



