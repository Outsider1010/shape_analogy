import largestinteriorrectangle as lir

from src.biframemethod.innerframefinder.InnerFrameFinder import InnerFrameFinder
from src.biframemethod.rectangle import Rectangle
from src.point import Point
from src.shapes.pixelShape import PixelShape

class BarycenterFrameFinder(InnerFrameFinder):

    def findInnerFramePixels(self, shape: PixelShape):

        # =================================================
        # Calculate the mean position of the border's form.
        # =================================================

        matrix = shape.getPixels()

        # ==========
        #   STEP 1
        # ==========
        # Identify the broder of the shape.
        rows, cols = len(matrix), len(matrix[0])
        boundary_points = []

        # Directions for the 4-neighbors (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for y in range(rows):
            for x in range(cols):
                if matrix[y][x] == 1:
                    # Check if this cell is a boundary cell
                    is_boundary = False
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        if ny < 0 or ny >= rows or nx < 0 or nx >= cols or matrix[ny][nx] == 0:
                            is_boundary = True
                            break
                    if is_boundary:
                        boundary_points.append((x, y))

        # ==========
        #   STEP 2
        # ==========

        # Calculate the centroid
        sum_x = sum(p[0] for p in boundary_points)
        sum_y = sum(p[1] for p in boundary_points)
        count = len(boundary_points)

        center = (sum_x / count, sum_y / count)

        # =================================================
        #                     Expand r
        # =================================================

        cx, cy = int(round(center[0])), int(round(center[1]))

        Hx, Hy = cx, cy
        Bx, By = cx, cy

        # Expand until it reaches the shape border.
        while True:
            moved = False
            if Hy > 0 and matrix[Hy - 1][Hx] == 1:
                Hy -= 1
                moved = True
            if By < rows - 1 and matrix[By + 1][Bx] == 1:
                By += 1
                moved = True
            if not moved:
                break

        width = Hx - Bx
        height = Hy - By

        return Rectangle.fromTopLeft(Point(Hx, Hy), width, height)