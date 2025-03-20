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

        # =================================================
        #         Expansion du rectangle intérieur
        # =================================================
        # Initialisation : un rectangle réduit au barycentre.
        Hx, Hy = Cx, Cy  # Coin supérieur gauche (top-left)
        Bx, By = Cx, Cy  # Coin inférieur droit (bottom-right)

        # Paramètres d'extension
        step = Decimal('0.1')
        tolerance = Decimal('0.001')

        # Fonction auxiliaire pour vérifier qu'un segment est entièrement dans la forme
        def segment_in_shape(x1: Decimal, y1: Decimal, x2: Decimal, y2: Decimal, num_samples: int = 5) -> bool:
            for i in range(num_samples + 1):
                t = Decimal(i) / Decimal(num_samples)
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                if not shape.isPointInShape(x, y):
                    return False
            return True

        def can_expand(Hx: Decimal, Hy: Decimal, Bx: Decimal, By: Decimal, step: Decimal) -> bool:
            new_Hx = Hx - step
            new_Hy = Hy + step
            new_Bx = Bx + step
            new_By = By - step

            # Vérification des coins
            if not shape.isPointInShape(new_Hx, new_Hy) or not shape.isPointInShape(new_Bx, new_By):
                return False
            # Vérification des segments horizontaux (haut et bas)
            if not segment_in_shape(new_Hx, new_Hy, new_Bx, new_Hy):
                return False
            if not segment_in_shape(new_Hx, new_By, new_Bx, new_By):
                return False
            # Vérification des segments verticaux (gauche et droite)
            if not segment_in_shape(new_Hx, new_By, new_Hx, new_Hy):
                return False
            if not segment_in_shape(new_Bx, new_By, new_Bx, new_Hy):
                return False

            return True

        # Boucle d'extension du rectangle tant que possible
        while step > tolerance:
            if can_expand(Hx, Hy, Bx, By, step):
                Hx -= step
                Hy += step
                Bx += step
                By -= step
            else:
                step = step / Decimal(2)

        width = Bx - Hx
        height = Hy - By
        rect = Rectangle.fromTopLeft(Point(Hx, Hy), width, height)
        print("Inner rectangle:", rect)
        return rect