from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point
from src.shapes.pixelShape import PixelShape
import numpy as np

def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)

class BarycenterRectangleFinder(InnerRectangleFinder):

    def findInnerRectanglePixels(self, shape: PixelShape):

        matrix = shape.pixels

        # =================================================
        #               Calculate the centroid
        # =================================================

        w2, h2 = shape.dim()

        # ==========
        #   STEP 1
        # ==========
        # Identify the border of the shape.
        h, w = shape.dim()

        ys, xs = np.where(matrix)

        ys2 = (h / 2 - ys) - .5
        xs2 = (xs - w / 2) + .5

        print(ys2, xs2)

        # ==========
        #   STEP 2
        # ==========
        # Calculate the centroid

        center = Point(np.mean(xs2), np.mean(ys2))

        print(center)

        Cx, Cy = center.x, center.y

        Cx, Cy = 1.5, 2.5

        # Look for the nearest point from center, which is also on the shape.
        if not shape.isPointInShape(Cx, Cy):


        print("nouvelles coordonnées : ", Cx, " : ", Cy)
        # =================================================
        #                     Expand r
        # =================================================

        Hx, Hy = Cx, Cy
        Bx, By = Cx, Cy

        moved = True

        #epsilon = .1
        step = .1

        # Expand until it reaches the shape border.
        while moved:

            moved = False

            if shape.isPointInShape(Hx - step, Hy + step):
                Hx -= step
                Hy += step
                moved = True

            if shape.isPointInShape(Bx + step, By - step):
                Bx += step
                By -= step
                moved = True

        width = Bx - Hx
        height = Hy - By

        rectangle = Rectangle.fromTopLeft(Point(Hx,Hy), width, height)
        print(rectangle)

        return rectangle
