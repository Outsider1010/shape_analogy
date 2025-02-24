import numpy as np

from src.birectangle.Rectangle import Rectangle
from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.shapes.pixelShape import PixelShape


def exactly_two_of_three(a: bool, b: bool, c: bool):
    return (a and b and not c) or (a and not b and c) or (not a and b and c)


class AxisMethodFinder(InnerRectangleFinder):

    def findInnerRectanglePixels(self, shape: PixelShape) -> Rectangle:

        matrix = shape.pixels

        # Identify the vertices of the shape.
        h, w = shape.dim()
        vertices = set()

        ys, xs = np.where(matrix)
        # python iterations on the matrix are NOT EFFICIENT
        # only iterate on pixels where there is the shape
        for i in range(xs.shape[0]):
            y = ys[i]
            x = xs[i]

            # Get the vertices (so a finite number of point) but doesn't work to compute the barycenter
            top = y - 1 < 0 or not matrix[y - 1, x]
            bottom = y + 1 >= h or not matrix[y + 1, x]
            left = x - 1 < 0 or not matrix[y, x - 1]
            right = x + 1 >= w or not matrix[y, x + 1]
            top_left = y - 1 < 0 or x - 1 < 0 or not matrix[y - 1, x - 1]
            top_right = y - 1 < 0 or x + 1 >= w or not matrix[y - 1, x + 1]
            bottom_left = y + 1 >= h or x - 1 < 0 or not matrix[y + 1, x - 1]
            bottom_right = y + 1 >= h or x + 1 >= w or not matrix[y + 1, x + 1]

            if (top and left) or exactly_two_of_three(not top, not left, not top_left):
                vertices.add((x, y))
            if (top and right) or exactly_two_of_three(not top, not right, not top_right):
                vertices.add((x + 1, y))
            if (bottom and left) or exactly_two_of_three(not bottom, not left, not bottom_left):
                vertices.add((x, y + 1))
            if (bottom and right) or exactly_two_of_three(not bottom, not right, not bottom_right):
                vertices.add((x + 1, y + 1))

        vertices = np.array([[a, b] for a, b in vertices])

        return Rectangle(0, 0, 0, 0)