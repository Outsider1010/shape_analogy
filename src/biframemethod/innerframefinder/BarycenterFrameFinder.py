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
        rows, cols = shape.dim()
        boundary_points = set()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ys, xs = np.where(matrix)

        # python iterations on the matrix are NOT EFFICIENT
        # only iterate on pixels where there is the shape
        for i in range(xs.shape[0]):
            y = ys[i]
            x = xs[i]

            # Get the vertices (so a finite number of point) but doesn't work to compute the barycenter
            top = y - 1 < 0 or not matrix[y - 1, x]
            bottom = y + 1 >= rows or not matrix[y + 1, x]
            left = x - 1 < 0 or not matrix[y, x - 1]
            right = x + 1 >= cols or not matrix[y, x + 1]
            top_left = y - 1 < 0 or x - 1 < 0 or not matrix[y - 1, x - 1]
            top_right = y - 1 < 0 or x + 1 >= cols or not matrix[y - 1, x + 1]
            bottom_left = y + 1 >= rows or x - 1 < 0 or not matrix[y + 1, x - 1]
            bottom_right = y + 1 >= rows or x + 1 >= cols or not matrix[y + 1, x + 1]

            if (top and left) or exactly_two_of_three(not top, not left, not top_left):
                boundary_points.add((int(x), int(y)))
            if (top and right) or exactly_two_of_three(not top, not right, not top_right):
                boundary_points.add((int(x) + 1, int(y)))
            if (bottom and left) or exactly_two_of_three(not bottom, not left, not bottom_left):
                boundary_points.add((int(x), int(y) + 1))
            if (bottom and right) or exactly_two_of_three(not bottom, not right, not bottom_right):
                boundary_points.add((int(x) + 1, int(y) + 1))

            # DOESN'T WORK PIXELS AREN'T POINTS. There are infinitely many points on the border
            # Check if this cell is a boundary cell
            # is_boundary = False
            # for dy, dx in directions:
            #     ny, nx = y + dy, x + dx
            #     if ny < 0 or ny >= rows or nx < 0 or nx >= cols or not matrix[ny, nx]:
            #         is_boundary = True
            #         break
            # if is_boundary:
            #     boundary_points.add((x, y))

        # ==========
        #   STEP 2
        # ==========
        # Calculate the centroid

        print(boundary_points)
        sum_x = sum(p[0] for p in boundary_points)
        sum_y = sum(p[1] for p in boundary_points)
        count = len(boundary_points)

        center = Point(sum_x / count - cols/2, rows/2 - sum_y / count)

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
            if By < rows - 1 and shape.isPointInShape(Bx, By + 1):
                By += 1
                moved = True
            if not moved:
                break

        return Rectangle.fromTopLeft(Point(Hx, Hy), Bx - Hx - cols/2, rows/2 - (By - Hy))