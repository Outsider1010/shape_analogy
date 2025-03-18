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
        self.rectangles = set(rects)

    def addRectangle(self, r: Rectangle):
        self.rectangles.add(r)

    def __add__(self, other):
        return UnionRectangles(self.rectangles.union(other.rectangles))

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
            y_min = min(y_min, r.x_min)
            y_max = max(y_max, r.x_max)
        return Rectangle(x_min, x_max, y_min, y_max)

    def getInnerRectangle(self, strategy) -> Rectangle:
        return strategy.findInnerRectangleUnionR(self)

    def fromShape(self, frame: Rectangle):
        res = UnionRectangles()
        for r in self.rectangles:
            x_min = max(frame.x_min, r.x_min)
            x_max = min(frame.x_max, r.x_max)
            y_min = max(frame.y_min, r.y_min)
            y_max = min(frame.y_max, r.y_max)
            if x_min < x_max and y_min < y_max:
                res.addRectangle(Rectangle(x_min, x_max, y_min, y_max))
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

    def toPixels(self) -> {}:
        # 1. On calcule le rectangle englobant.
        outer = self.getOuterRectangle()

        x_min = float(outer.x_min)
        x_max = float(outer.x_max)
        y_min = float(outer.y_min)
        y_max = float(outer.y_max)

        # Bornes pour la grille de pixels.
        px_min = math.floor(x_min)
        px_max = math.ceil(x_max)
        py_min = math.floor(y_min)
        py_max = math.ceil(y_max)

        width = px_max - px_min
        height = py_max - py_min

        # 2. On initialise la matrice de pixels.
        pixels = np.zeros((height, width), dtype = np.uint8)

        # 3. On parcourt chaque rectangle.
        for rect in self.rectangles:
            rx_min = float(rect.x_min)
            rx_max = float(rect.x_max)
            ry_min = float(rect.y_min)
            ry_max = float(rect.y_max)

            # Indices pour la zone du rectangle dans la matrice.
            # Par exemple pour i_max = min(width, math.ceil(rx_max) - px_min) :
            #   math.ceil(rx_max): prend la valeur entière supérieure de rx_max pour inclure le dernier pixel.
            #   - px_min: ajuste par rapport à l'origine de la matrice (repère cartésien).
            #   min(width, ...): nous empêche de dépasser la largeur de la matrice.
            i_min = max(0, math.floor(rx_min) - px_min)
            i_max = min(width, math.ceil(rx_max) - px_min)
            j_min = max(0, math.floor(ry_min) - py_min)
            j_max = min(height, math.ceil(ry_max) - py_min)

            for j in range(j_min, j_max):
                for i in range(i_min, i_max):
                    pixel_x_min = px_min + i
                    pixel_x_max = pixel_x_min + 1
                    pixel_y_min = py_min + j
                    pixel_y_max = pixel_y_min + 1

                    inter_x_min = max(rx_min, pixel_x_min)
                    inter_x_max = min(rx_max, pixel_x_max)
                    inter_y_min = max(ry_min, pixel_y_min)
                    inter_y_max = min(ry_max, pixel_y_max)

                    inter_width = max(0, inter_x_max - inter_x_min)
                    inter_height = max(0, inter_y_max - inter_y_min)
                    inter_area = inter_width * inter_height

                    coverage = inter_area

                    # Calcul de la teinte :
                    # Si le pixel est totalement recouvert (coverage == 1), valeur = 255,
                    # Sinon pour un recouvrement partiel, valeur = coverage * 255.
                    new_value = int(round(coverage * 255))

                    # Comme le pixel peut être recouvert par plusieurs rectangles, on garde le maximum.
                    pixels[j, i] = max(pixels[j, i], new_value)

        return pixels

    def toImage(self, name: str = "default.bmp"):
        self.toPixels().toImage(name)

    def toSinogram(self, maxAngle: float = 180.):
        # TODO
        pass
