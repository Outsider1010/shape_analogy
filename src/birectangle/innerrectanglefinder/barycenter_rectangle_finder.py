from decimal import Decimal

import numpy as np

from src.birectangle.innerrectanglefinder.inner_rectangle_finder import *
from src.birectangle.point import Point
from src.birectangle.Segment import Segment


def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)


class BarycenterRectangleFinder(InnerRectangleFinder):

    def findInnerRectanglePixels(self, shape : PixelShape) -> Rectangle:
        matrix = shape.pixels
        h, w = shape.dim()

        # Pré-calculer les moitiés en Decimal.
        half_h = Decimal(h) / Decimal(2)
        half_w = Decimal(w) / Decimal(2)
        dec_half = Decimal('0.5')

        # =================================================
        #               Calcul du barycentre
        # =================================================
        ys_idx, xs_idx = np.where(matrix)
        # Convertir en Decimal et ajuster pour obtenir les coordonnées
        xs_dec = [Decimal(x) - (Decimal(w) / Decimal(2)) + dec_half for x in xs_idx]
        ys_dec = [half_h - Decimal(y) - dec_half for y in ys_idx]

        # Calculer la moyenne avec une somme en Decimal
        if xs_dec and ys_dec:
            sum_x = sum(xs_dec, Decimal(0))
            sum_y = sum(ys_dec, Decimal(0))
            count = Decimal(len(xs_dec))
            center_x = sum_x / count
            center_y = sum_y / count
        else:
            # Cas où la forme est vide
            center_x, center_y = Decimal(0), Decimal(0)

        center = Point(center_x, center_y)
        print("Center init :", center)
        Cx, Cy = center.x, center.y

        # Si le centre n'est pas dans la forme, recherche du pixel le plus proche.
        if not shape.isPointInShape(Cx, Cy):
            # Conserver la liste des points sous forme de tuples de Decimal.
            points = list(zip(xs_dec, ys_dec))
            # Calculer la distance au carré (on compare sans racine)
            def sq_distance(p):
                return (p[0] - Cx) ** 2 + (p[1] - Cy) ** 2
            nearest_idx = min(range(len(points)), key=lambda i: sq_distance(points[i]))
            nearestPixel = list(points[nearest_idx])  # on transforme en liste pour modification
            print("Pixel le plus proche :", nearestPixel)

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
        # Initialisation : on part d'un rectangle réduit à un point.
        Hx, Hy = Cx, Cy  # Coin supérieur gauche (top-left).
        Bx, By = Cx, Cy  # Coin inférieur droit (bottom-right).

        initial_step = Decimal('0.1')
        step = initial_step
        tolerance = Decimal('0.001')

        def can_expand(Hx, Hy, Bx, By, step):
            """
            Vérifie si en étendant le rectangle d'un pas donné le long
            de la diagonale de pente -1, le rectangle reste dans la forme.
            """
            new_Hx = Hx - step
            new_Hy = Hy + step
            new_Bx = Bx + step
            new_By = By - step

            # Vérification des coins.
            if not shape.isPointInShape(new_Hx, new_Hy) or not shape.isPointInShape(new_Bx, new_By):
                return False

            # Vérification des segments horizontaux (haut et bas).
            top_seg = Segment(Point(new_Hx, new_Hy), Point(new_Bx, new_Hy))
            bottom_seg = Segment(Point(new_Hx, new_By), Point(new_Bx, new_By))
            if not shape.isHorizontalSegmentInShape(top_seg) or not shape.isHorizontalSegmentInShape(bottom_seg):
                return False

            # Vérification des segments verticaux (gauche et droite).
            left_seg = Segment(Point(new_Hx, new_By), Point(new_Hx, new_Hy))
            right_seg = Segment(Point(new_Bx, new_By), Point(new_Bx, new_Hy))
            if not shape.isVerticalSegmentInShape(left_seg) or not shape.isVerticalSegmentInShape(right_seg):
                return False

            return True

        # Boucle d'extension.
        while step > tolerance:
            if can_expand(Hx, Hy, Bx, By, step):
                # On peut étendre : on met à jour les coins.
                Hx -= step
                Hy += step
                Bx += step
                By -= step
            else:
                # On dépasse : on réduit le pas.
                step = step / Decimal(2)

        width = Bx - Hx
        height = Hy - By
        rectangle = Rectangle.fromTopLeft(Point(Hx, Hy), width, height)
        print(rectangle)
        return rectangle

    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        # =================================================
        #      Calcul du barycentre par moyenne pondérée
        # =================================================
        total_area = Decimal('0')
        sum_x = Decimal('0')
        sum_y = Decimal('0')
        for r in shape.rectangles:
            width = r.x_max - r.x_min
            height = r.y_max - r.y_min
            area = width * height
            center = r.center()  # retourne un Point avec des Decimal
            total_area += area
            sum_x += center.x * area
            sum_y += center.y * area

        if total_area > 0:
            center_x = sum_x / total_area
            center_y = sum_y / total_area
        else:
            center_x = Decimal('0')
            center_y = Decimal('0')

        center = Point(center_x, center_y)
        print("Center init:", center)
        Cx, Cy = center.x, center.y

        # Si le barycentre n'est pas dans la forme, on choisit le centre du rectangle
        # le plus proche (en distance euclidienne)
        if not shape.isPointInShape(Cx, Cy):
            min_dist = None
            nearest_center = None
            for r in shape.rectangles:
                pt = r.center()
                dist_sq = (pt.x - Cx) ** 2 + (pt.y - Cy) ** 2
                if min_dist is None or dist_sq < min_dist:
                    min_dist = dist_sq
                    nearest_center = pt
            center = nearest_center
            Cx, Cy = center.x, center.y
            print("Adjusted center:", center)
        else:
            print("Center inside shape:", center)

        left, right, top, bottom = Cx, Cx, Cy, Cy

        def vertical_segment_in_shape(x: Decimal, y_bottom: Decimal, y_top: Decimal, num_samples: int = 10) -> bool:
            for i in range(num_samples + 1):
                t = Decimal(i) / Decimal(num_samples)
                y = y_bottom + (y_top - y_bottom) * t
                if not shape.isPointInShape(x, y):
                    return False
            return True

        def horizontal_segment_in_shape(y: Decimal, x_left: Decimal, x_right: Decimal, num_samples: int = 10) -> bool:
            for i in range(num_samples + 1):
                t = Decimal(i) / Decimal(num_samples)
                x = x_left + (x_right - x_left) * t
                if not shape.isPointInShape(x, y):
                    return False
            return True

        initial_step = Decimal('0.1')
        tolerance = Decimal('0.001')

        # Expansion du bord gauche
        step = initial_step
        while step > tolerance:
            new_left = left - step
            if vertical_segment_in_shape(new_left, bottom, top):
                left = new_left
            else:
                step = step / Decimal(2)

        # Expansion du bord droit
        step = initial_step
        while step > tolerance:
            new_right = right + step
            if vertical_segment_in_shape(new_right, bottom, top):
                right = new_right
            else:
                step = step / Decimal(2)

        # Expansion du bord supérieur (top)
        step = initial_step
        while step > tolerance:
            new_top = top + step
            if horizontal_segment_in_shape(new_top, left, right):
                top = new_top
            else:
                step = step / Decimal(2)

        # Expansion du bord inférieur (bottom)
        step = initial_step
        while step > tolerance:
            new_bottom = bottom - step
            if horizontal_segment_in_shape(new_bottom, left, right):
                bottom = new_bottom
            else:
                step = step / Decimal(2)

        # --- Tentative de restriction aux carrés 1×1 ---
        # On va essayer d'arrondir left, right, top, bottom aux entiers (selon un sens cohérent)
        from math import floor, ceil

        snapped_left = Decimal(floor(left))
        snapped_right = Decimal(ceil(right))
        snapped_bottom = Decimal(floor(bottom))
        snapped_top = Decimal(ceil(top))

        # On vérifie si le snapping donne un rectangle entièrement dans la forme
        if (vertical_segment_in_shape(snapped_left, snapped_bottom, snapped_top) and
                vertical_segment_in_shape(snapped_right, snapped_bottom, snapped_top) and
                horizontal_segment_in_shape(snapped_top, snapped_left, snapped_right) and
                horizontal_segment_in_shape(snapped_bottom, snapped_left, snapped_right)):
            # On adopte la version "snap"
            left, right, bottom, top = snapped_left, snapped_right, snapped_bottom, snapped_top

        # --- Construction finale du rectangle ---
        width = right - left
        height = top - bottom
        # On construit le rectangle à partir du coin supérieur gauche
        result = Rectangle.fromTopLeft(Point(left, top), width, height)
        return result