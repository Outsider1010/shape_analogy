from src.biframemethod.innerframefinder.InnerFrameFinder import InnerFrameFinder
from src.biframemethod.rectangle import Rectangle
from src.biframemethod.point import Point
from src.shapes.pixelShape import PixelShape
import numpy as np

def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)

class BarycenterFrameFinder(InnerFrameFinder):

    def findInnerFramePixels(self, shape: PixelShape):

        # =================================================
        # Calculate the mean position of the border's form. (form ?)
        # =================================================

        matrix = shape.pixelsMatrix()
        # ==========
        #   STEP 1
        # ==========
        # Identify the border of the shape.
        h, w = shape.dim()

        ys, xs = np.where(matrix)
        ys = h / 2 - ys
        xs = xs - w / 2

        # ==========
        #   STEP 2
        # ==========
        # Calculate the centroid

        center = Point(np.mean(ys), np.mean(xs))

        print(center)
        # =================================================
        #                     Expand r
        # =================================================

        Hx, Hy = center.x, center.y
        Bx, By = center.x, center.y

        # Expand until it reaches the shape border.
        while True:
            moved = False
            if Hy > 0 and shape.isPointInShape(Hx, Hy - 1):
                Hy -= 1
                moved = True
            if By < h - 1 and shape.isPointInShape(Bx, By + 1):
                By += 1
                moved = True
            if not moved:
                break

        return Rectangle.fromTopLeft(Point(Hx, Hy), Bx - Hx - w/2, h/2 - (By - Hy))