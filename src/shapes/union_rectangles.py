import math
from decimal import Decimal

import numpy as np

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
import src.shapes.pixel_shape as ps
from .shape import Shape
from ..birectangle.point import Point
from math import ceil, floor

# DO NOT IMPORT STRATEGIES (to avoid circular imports)

def calculate_active_length(active_intervals):
    if not active_intervals:
        return 0
    active_intervals.sort()
    total_length = 0
    current_start = active_intervals[0][0]
    current_end = active_intervals[0][1]
    for start, end in active_intervals[1:]:
        if start > current_end:
            total_length += current_end - current_start
            current_start = start
            current_end = end
        else:
            current_end = max(current_end, end)
    total_length += current_end - current_start
    return total_length


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
        # possibly_alr_included = self.size() > 0 and self.getOuterRectangle().containsRectangle(r)
        # if not possibly_alr_included or all(not x.containsRectangle(r) for x in self.rectangles):
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

    def outer_rectangle(self) -> Rectangle:
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
        if self.size() == 0:
            return res
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
            r.plotFilled(color, 2)

    def union_area(self):
        # Define events for the sweep line algorithm
        events = []
        for rect in self.rectangles:
            x1, x2, y1, y2 = rect
            events.append((x1, y1, y2, 'start'))
            events.append((x2, y1, y2, 'end'))

        # Sort events by x-coordinate, breaking ties by 'end' before 'start'
        events.sort(key=lambda ev_x: (ev_x[0], ev_x[3] == 'start'))

        # Process events with the sweep line algorithm
        active_intervals = []
        total_area = 0
        prev_x = None

        for x, y1, y2, event_type in events:
            if prev_x is not None:
                active_length = calculate_active_length(active_intervals)
                total_area += active_length * (x - prev_x)

            if event_type == 'start':
                active_intervals.append((y1, y2))
            else:
                active_intervals.remove((y1, y2))
            prev_x = x

        return total_area

    def toPixels(self):
        # 1. Calcul du rectangle englobant et de la grille.
        w = 2 * math.ceil(max(abs(self.x_min), abs(self.x_max)))
        h = 2 * math.ceil(max(abs(self.y_min), abs(self.y_max)))
        w = max(w, 2)
        h = max(h, 2)
        grid_x_min = -w / 2
        grid_y_min = -h / 2

        # On fait une conversion en decimal.
        grid_x_min_dec = Decimal(grid_x_min)
        grid_y_min_dec = Decimal(grid_y_min)

        # 2. Initialise la matrice de pixels en blanc.
        pixels = np.full((h, w), 255, dtype=np.uint8)

        # Dictionnaire pour les pixels partiellement couverts :
        # Clef = (i,j), valeur = liste de morceaux (instances de Rectangle) ou None si pixel totalement couvert.
        partial_pixels = {}

        # 3. Parcours des rectangles pour marquer les pixels totalement recouverts et accumuler les morceaux.
        for rect in self.rectangles:
            # Conversion des coordonnées du rectangle en indices de pixels.
            i_min = int(math.floor(float(rect.x_min - grid_x_min_dec)))
            i_max = int(math.ceil(float(rect.x_max - grid_x_min_dec)))
            j_min = int(math.floor(float(rect.y_min - grid_y_min_dec)))
            j_max = int(math.ceil(float(rect.y_max - grid_y_min_dec)))

            for j in range(max(0, j_min), min(h, j_max)):
                for i in range(max(0, i_min), min(w, i_max)):
                    # Définition des bords du pixel en coordonnées réelles.
                    pixel_x_min = grid_x_min + i
                    pixel_y_min = grid_y_min + j
                    pixel_x_max = pixel_x_min + 1
                    pixel_y_max = pixel_y_min + 1

                    # Intersection entre le pixel et le rectangle.
                    inter_x_min = max(rect.x_min, Decimal(pixel_x_min))
                    inter_x_max = min(rect.x_max, Decimal(pixel_x_max))
                    inter_y_min = max(rect.y_min, Decimal(pixel_y_min))
                    inter_y_max = min(rect.y_max, Decimal(pixel_y_max))
                    inter_width = max(Decimal(0), inter_x_max - inter_x_min)
                    inter_height = max(Decimal(0), inter_y_max - inter_y_min)

                    if inter_width <= 0 or inter_height <= 0:
                        continue

                    # Si le pixel est entièrement recouvert par le rectangle.
                    if rect.x_min <= Decimal(pixel_x_min) and rect.x_max >= Decimal(pixel_x_max) and \
                            rect.y_min <= Decimal(pixel_y_min) and rect.y_max >= Decimal(pixel_y_max):
                        pixels[j, i] = 0
                        # Marque le pixel comme totalement couvert en mettant None.
                        partial_pixels[(i, j)] = None
                    else:
                        #  Ajoute le morceau si le pixel n'est pas déjà marqué comme totalement couvert.
                        if (i, j) in partial_pixels and partial_pixels[(i, j)] is None:
                            continue

                        morceau = Rectangle(inter_x_min, inter_x_max, inter_y_min, inter_y_max)
                        if (i, j) not in partial_pixels:
                            partial_pixels[(i, j)] = UnionRectangles()
                        partial_pixels[(i, j)].addRectangle(morceau)

        # 4. Pour chaque pixel partiellement couvert, on calcule la fraction de recouvrement.
        for (i, j), union_rect in partial_pixels.items():
            if partial_pixels[(i, j)] is not None:
                covered_area = union_rect.union_area()
                covered_area = min(covered_area, 1)
                new_value = round(255 * (1 - covered_area))

                pixels[j, i] = new_value

        return ps.PixelShape(array=pixels)

    def toImage(self, name: str = "default.bmp"):
        self.toPixels().toImage(name)

    def toSinogram(self, maxAngle: float = 180.):
        # TODO
        pass

    def size(self):
        return len(self.rectangles)
