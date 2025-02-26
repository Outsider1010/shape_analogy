from src.birectangle.Segment import Segment
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
        #               Calculating the centroid
        # =================================================

        h, w = shape.dim()

        ys, xs = np.where(matrix)

        ys = (h / 2 - ys) - .5
        xs = (xs - w / 2) + .5

        center = Point(np.mean(xs), np.mean(ys))

        print("Center init : ", center)

        Cx, Cy = center.x, center.y

        # Test
        # Cx, Cy = 3, 1.5

        # Look for the nearest point from center, which is also on the shape.
        if not shape.isPointInShape(Cx, Cy):
            # [1.] Finding the nearest pixel's center.

            points = np.array([xs, ys]).T
            print(points)

            distances = np.linalg.norm(points - np.array([Cx, Cy]), axis=1)
            nearest_idx = np.argmin(distances)
            nearestPixel = points[nearest_idx]

            print("Pixel le plus proche : ", nearestPixel)

            # [2.] Moving the newfound point to the nearest extremity of the pixel's border.

            dx = Cx - nearestPixel[0]
            dy = Cy - nearestPixel[1]

            # Conditions
            dx_positive = dx > 0
            dx_more_half_pix_size = np.abs(dx) >= .5

            dy_positive = dy > 0
            dy_more_half_pix_size = np.abs(dy) >= .5

            if dx_more_half_pix_size:
                if dx_positive:
                    nearestPixel[0] += .5
                else:
                    nearestPixel[0] -= .5

            if dy_positive:
                if dy_more_half_pix_size:
                    nearestPixel[1] += .5
                else:
                    nearestPixel[1] -= .5

            center = Point(nearestPixel[0], nearestPixel[1])
            Cx, Cy = center.x, center.y

            # [3.] Finding the longest segment.


        print("Center : ", center)

        # =================================================
        #                   Expanding r
        # =================================================

        Hx, Hy = Cx, Cy
        Bx, By = Cx, Cy

        moved = True

        #epsilon = .1
        step = .1

        # Expand until it reaches the shape border.
        while moved:
            moved = False

            # [1.] Left above point
            H_in_shape = shape.isPointInShape(Hx - step, Hy + step)
            aboveSeg = Segment(Point(Hx - step, Hy + step), Point(Bx, Hy + step))
            belowSeg = Segment(Point(Hx - step, By), Point(Bx, By))
            aboveSeg_in_shape = shape.isHorizontalSegmentInShape(aboveSeg)
            belowSeg_in_shape = shape.isHorizontalSegmentInShape(belowSeg)
            if H_in_shape and aboveSeg_in_shape and belowSeg_in_shape:
                Hx -= step
                Hy += step
                moved = True

            # [2.] Right bottom point
            B_in_shape =  shape.isPointInShape(Bx + step, By - step)
            leftSeg = Segment(Point(Hx, By), Point(Hx, Hy))
            rightSeg = Segment(Point(Bx, By), Point(Bx, Hy))
            leftSeg_in_shape = shape.isVerticalSegmentInShape(leftSeg)
            rightSeg_in_shape = shape.isVerticalSegmentInShape(rightSeg)
            if B_in_shape and leftSeg_in_shape and rightSeg_in_shape:
                Bx += step
                By -= step
                moved = True

        width = Bx - Hx
        height = Hy - By

        rectangle = Rectangle.fromTopLeft(Point(Hx,Hy), width, height)
        print(rectangle)

        return rectangle
