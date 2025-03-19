import math
from decimal import Decimal
from typing import Iterable

import numpy as np

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from .shape import Shape
# DO NOT IMPORT STRATEGIES (to avoid circular imports)

class UnionRectangles(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """
    def __init__(self, rects: Iterable[Rectangle] = None):
        if rects is None:
            self.rectangles = []
        else:
            self.rectangles = list(rects)

    def addRectangle(self, r: Rectangle):
        self.rectangles.append(r)

    def __add__(self, other):
        return UnionRectangles(self.rectangles + other.rectangles)

    def __repr__(self):
        return str(self.rectangles)

    def getOuterRectangle(self) -> Rectangle:
        if len(self.rectangles) == 0:
            return Rectangle(0, 0, 0, 0)
        i = iter(self.rectangles)
        r = next(i)
        x_min, x_max,y_min, y_max = r
        r = next(i, None)
        while r:
            x_min = min(x_min, r.x_min)
            x_max = max(x_max, r.x_max)
            y_min = min(y_min, r.y_min)
            y_max = max(y_max, r.y_max)
            r = next(i, None)
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectangleUnionR(self)

    def fromShape(self, frame: Rectangle):
        res = UnionRectangles()
        for r in self.rectangles:
            x = frame.intersection(r)
            if x is not None and x.area() > 0:
                res.addRectangle(x)
        return res

    def equiv(self, fromCoordSysR: Rectangle | None, toCoordSysR: Rectangle | None):
        if fromCoordSysR is None or toCoordSysR is None:
            return self
        else:
            res = UnionRectangles()
            for r in self.rectangles:
                b = BiRectangle(fromCoordSysR, r)
                res.addRectangle(b.innerEquiv(toCoordSysR))
            return res

    def isPointInShape(self, x: Decimal | float, y: Decimal | float) -> bool:
        return any(r.isPointInRectangle(x, y) for r in self.rectangles)

    def __eq__(self, other):
        if not isinstance(other, UnionRectangles):
            return False
        # TODO
        pass

    def isEmpty(self) -> bool:
        return len(self.rectangles) == 0

    def plot(self) -> None:
        for r in self.rectangles:
            r.plotFilled("k", 1)

    def union_area(self, rects):
        """
            Calcule l'aire de l'union d'une liste de rectangles (définis par (x_min, x_max, y_min, y_max))
            en découpant le domaine en intervalles sur les axes x et y.
        """
        if not rects:
            return 0

        # On récupère tous les abscisses et ordonnées de bords.
        xs = sorted(set([r[0] for r in rects] + [r[1] for r in rects]))
        ys = sorted(set([r[2] for r in rects] + [r[3] for r in rects]))

        area = 0
        # Pour chaque sous-rectangle formé par ces coupures.
        for i in range(len(xs) - 1):
            for j in range(len(ys) - 1):
                cell_x_min, cell_x_max = xs[i], xs[i + 1]
                cell_y_min, cell_y_max = ys[j], ys[j + 1]
                # Vérifie si ce petit rectangle est couvert par au moins un rectangle de la liste.
                # On prend le centre du petit rectangle pour le test.
                cx = (cell_x_min + cell_x_max) / 2
                cy = (cell_y_min + cell_y_max) / 2
                for (rx_min, rx_max, ry_min, ry_max) in rects:
                    if rx_min <= cx <= rx_max and ry_min <= cy <= ry_max:
                        area += (cell_x_max - cell_x_min) * (cell_y_max - cell_y_min)
                        break
        return area

    def toPixels(self) -> np.ndarray:
        # 1. Calcule le rectangle englobant.
        outer = self.getOuterRectangle()

        x_min_outer = float(outer.x_min)
        x_max_outer = float(outer.x_max)
        y_min_outer = float(outer.y_min)
        y_max_outer = float(outer.y_max)

        # 2. Détermine la taille de la grille de pixels.
        w = 2 * math.ceil(max(abs(x_min_outer), abs(x_max_outer)))
        h = 2 * math.ceil(max(abs(y_min_outer), abs(y_max_outer)))
        w = max(w, 2)
        h = max(h, 2)

        # La grille est centrée, donc:
        # Le coin inférieur gauche en coordonnées réelles est (-w/2, -h/2)
        grid_x_min = -w / 2
        grid_y_min = -h / 2

        # 3. Initialise la matrice de pixels en blanc.
        pixels = np.full((h, w), 255, dtype=np.uint8)

        # 4. Parcours de chaque pixel et calcul de l'union des zones couvertes par les rectangles.
        for j in range(h):
            for i in range(w):
                # Définition des bords du pixel en coordonnées réelles.
                pixel_x_min = grid_x_min + i
                pixel_x_max = pixel_x_min + 1
                pixel_y_min = grid_y_min + j
                pixel_y_max = pixel_y_min + 1

                # On calcule la liste des intersections entre le pixel et chaque rectangle.
                intersections = []
                for rect in self.rectangles:
                    rx_min = float(rect.x_min)
                    rx_max = float(rect.x_max)
                    ry_min = float(rect.y_min)
                    ry_max = float(rect.y_max)

                    # Calcul de l'intersection entre le pixel et le rectangle.
                    inter_x_min = max(rx_min, pixel_x_min)
                    inter_x_max = min(rx_max, pixel_x_max)
                    inter_y_min = max(ry_min, pixel_y_min)
                    inter_y_max = min(ry_max, pixel_y_max)

                    inter_width = max(0, inter_x_max - inter_x_min)
                    inter_height = max(0, inter_y_max - inter_y_min)

                    if inter_width > 0 and inter_height > 0:
                        intersections.append((inter_x_min, inter_x_max, inter_y_min, inter_y_max))

                # Calcul de l'aire totale couverte dans le pixel (union des zones).
                covered_area = self.union_area(intersections)

                # L'air est comprise entre 0 et 1 mais parfois la valeur numérique peut déborder, donc je fais un min.
                covered_area = min(covered_area, 1)

                # Calcule la nouvelle valeur de teinte en fonction de la fraction de recouvrement.
                new_value = 255 - int(round(covered_area * 255))
                pixels[j, i] = new_value

        return pixels

    def toImage(self, name: str = "default.bmp"):
        self.toPixels().toImage(name)

    def toSinogram(self, maxAngle: float = 180.):
        # TODO
        pass
