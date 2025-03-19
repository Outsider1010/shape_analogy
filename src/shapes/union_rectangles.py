import math
from decimal import Decimal

import numpy as np

from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
import src.shapes.pixel_shape as ps
from .shape import Shape
from ..birectangle.Point import Point


# DO NOT IMPORT STRATEGIES (to avoid circular imports)

class UnionRectangles(Shape):
    """
    Representation of shapes using a boolean matrix with even dimensions.
    Each pixel is a square of length 1 and equals True if it is included in the shape
    """
    def __init__(self):
        self.rectangles = []
        self.x_min = self.y_min = np.inf
        self.x_max = self.y_max = -np.inf

    def __setup(self, rectangles, x_min, x_max, y_min, y_max):
        self.rectangles = rectangles
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def addRectangle(self, r: Rectangle):
        possibly_alr_included = self.size() > 0 and self.getOuterRectangle().containsRectangle(r)
        if not possibly_alr_included or all(not x.containsRectangle(r) for x in self.rectangles):
            self.rectangles.append(r)
            self.x_min = min(self.x_min, r.x_min)
            self.x_max = max(self.x_max, r.x_max)
            self.y_min = min(self.y_min, r.y_min)
            self.y_max = max(self.y_max, r.y_max)

    def __add__(self, other):
        res = UnionRectangles()
        res.__setup(self.rectangles + other.rectangles, min(self.x_min, other.x_min), max(self.x_max, other.x_max),
                    min(self.y_min, other.y_min), max(self.y_max, other.y_max))
        return res

    def __repr__(self):
        return str(self.rectangles)

    def getOuterRectangle(self) -> Rectangle:
        if len(self.rectangles) == 0:
            return Rectangle(0, 0, 0, 0)
        return Rectangle(self.x_min, self.x_max, self.y_min, self.y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectangleUnionR(self)

    def fromShape(self, frame: Rectangle):
        res = UnionRectangles()
        new_rectangles = []
        x_min = y_min = np.inf
        x_max = y_max = -np.inf
        for r in self.rectangles:
            inter = frame.intersection(r)
            if inter is not None and inter.area() > 0:
                new_rectangles.append(inter)
                x_min = min(x_min, inter.x_min)
                x_max = max(x_max, inter.x_max)
                y_min = min(y_min, inter.y_min)
                y_max = max(y_max, inter.y_max)
        res.__setup(new_rectangles, x_min, x_max, y_min, y_max)
        return res

    def equiv(self, fromCoordSysR: Rectangle | None, toCoordSysR: Rectangle | None):
        res = UnionRectangles()
        if fromCoordSysR is None or toCoordSysR is None:
            res.__setup(self.rectangles.copy(), self.x_min, self.x_max, self.y_min, self.y_max)
        else:
            res = UnionRectangles()
            x_min, y_min = Point(self.x_min, self.y_min).toCoordSys(fromCoordSysR, toCoordSysR)
            x_max, y_max = Point(self.x_max, self.y_max).toCoordSys(fromCoordSysR, toCoordSysR)
            res.__setup([BiRectangle(fromCoordSysR, r).innerEquiv(toCoordSysR) for r in self.rectangles],
                        x_min, x_max, y_min, y_max)
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

    def plot(self, color='k') -> None:
        for r in self.rectangles:
            r.plotFilled(color, 1)

    def toPixels(self):
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

        # 3. Initialise la matrice de pixels.
        pixels = np.full((h, w), 255, dtype=np.uint8)

        # 4. Pour chaque rectangle, on détermine la zone respective de la matrice.
        for rect in self.rectangles:
            rx_min = float(rect.x_min)
            rx_max = float(rect.x_max)
            ry_min = float(rect.y_min)
            ry_max = float(rect.y_max)

            # Conversion des bornes réelles en indices de matrice.
            i_min = max(0, math.floor(rx_min - grid_x_min))
            i_max = min(w, math.ceil(rx_max - grid_x_min))
            j_min = max(0, math.floor(ry_min - grid_y_min))
            j_max = min(h, math.ceil(ry_max - grid_y_min))

            for j in range(j_min, j_max):
                for i in range(i_min, i_max):
                    # Bornes en coordonnées réelles du pixel.
                    pixel_x_min = grid_x_min + i
                    pixel_x_max = pixel_x_min + 1
                    pixel_y_min = grid_y_min + j
                    pixel_y_max = pixel_y_min + 1

                    # Puis on calcule l'intersection entre le pixel et le rectangle.
                    inter_x_min = max(rx_min, pixel_x_min)
                    inter_x_max = min(rx_max, pixel_x_max)
                    inter_y_min = max(ry_min, pixel_y_min)
                    inter_y_max = min(ry_max, pixel_y_max)

                    inter_width = max(0, inter_x_max - inter_x_min)
                    inter_height = max(0, inter_y_max - inter_y_min)
                    # Aire de l'intersection.
                    inter_area = inter_width * inter_height

                    # Calcule de la fraction de recouvrement.
                    coverage = inter_area
                    new_value = 255 - int(round(coverage * 255))

                    # Heuristique : si plusieurs rectangles recouvrent le même pixel, on garde la teinte la plus sombre.
                    pixels[j, i] = min(pixels[j, i], new_value)

        return ps.PixelShape(array=pixels)

    def toImage(self, name: str = "default.bmp"):
        self.toPixels().toImage(name)

    def toSinogram(self, maxAngle: float = 180.):
        # TODO
        pass

    def size(self):
        return len(self.rectangles)
