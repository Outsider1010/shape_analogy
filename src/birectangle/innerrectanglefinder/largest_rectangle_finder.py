
import numpy as np
from largestinteriorrectangle import lir

from src.birectangle.innerrectanglefinder.inner_rectangle_finder import InnerRectangleFinder
from src.birectangle.rectangle import Rectangle
from src.birectangle.point import Point
from src.shapes.union_rectangles import UnionRectangles

def largest_rect_in_histo(arr, xs, ys, y):
    n = arr.shape[0]
    s = []
    res = b_x = b_h = b_w = bfh = 0
    for i in range(n):
        while s and arr[s[-1]] >= arr[i]:
            # The popped item is to be considered as the smallest element of the histogram
            tp = s.pop()

            # For the popped item previous smaller element is just below it in the stack (or current stack top)
            # and next smaller element is i
            width = i if not s else i - s[-1] - 1
            x = 0 if not s else s[-1] + 1
            area = (ys[int(y - arr[tp] + 1)] - ys[y + 1]) * (xs[x + width] - xs[x])
            if area > res:
                res = area
                b_x = x
                bfh = arr[tp]
                b_h =  (ys[int(y - arr[tp] + 1)] - ys[y + 1])
                b_w = (xs[x + width] - xs[x])
        s.append(i)

    # For the remaining items in the stack, next smaller does
    # not exist. Previous smaller is the item just below in stack.
    while s:
        tp = s.pop()
        width = (n if not s else n - s[-1] - 1)
        x = 0 if not s else s[-1] + 1
        curr = (ys[int(y - arr[tp] + 1)] - ys[y + 1]) * (xs[x + width] - xs[x])
        if curr > res:
            res = curr
            b_x = x
            b_h = (ys[int(y - arr[tp] + 1)] - ys[y + 1])
            b_w = (xs[x + width] - xs[x])
            bfh = arr[tp]

    return res, b_x, b_h, b_w, bfh

# Function to find the maximum area of rectangle
# in a 2D matrix.
def lir_by_histogram(mat, xs, ys):
    n, m = mat.shape

    # Array to store matrix as a histogram.
    arr = np.zeros(m)

    ans = y = b_x = b_h = b_w = bfh = 0
    # Traverse row by row.
    for i in range(n):
        arr = np.where(mat[i], arr + 1, 0)
        if i == n - 1 or not np.all(mat[i + 1][mat[i] == 1] == 1):
            area, x, h, w, fh = largest_rect_in_histo(arr, xs, ys, i)
            if area > ans:
                ans = area
                y = i
                b_x = x
                b_h = h
                b_w = w
                bfh = fh
    return b_x, y - bfh + 1, b_w, b_h

class LargestRectangleFinder(InnerRectangleFinder):
    """
    Find the largest interior axis aligned rectangle of a shape.
    """

    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        if shape.size() == 0:
            return Rectangle(0, 0, 0, 0)
        xs = set()
        ys = set()
        for r in shape.rectangles:
            xs.add(r.x_min)
            xs.add(r.x_max)
            ys.add(r.y_min)
            ys.add(r.y_max)
        xs = sorted(xs)
        ys = sorted(ys, reverse=True)
        matrix = np.zeros((len(ys) - 1, len(xs) - 1), dtype=bool)
        for r in shape.rectangles:
            i_x_min = i_y_min = np.inf
            i_x_max = i_y_max = -np.inf
            for i, x in enumerate(xs):
                if x == r.x_min:
                    i_x_min = i
                if x == r.x_max:
                    i_x_max = i
            for i, y in enumerate(ys):
                if y == r.y_min:
                    i_y_max = i
                if y == r.y_max:
                    i_y_min = i
            matrix[i_y_min:i_y_max, i_x_min:i_x_max] = True

        x, y, w, h = lir_by_histogram(matrix, xs, ys)
        return Rectangle.fromTopLeft(Point(xs[x], ys[int(y)]), w, h)

    def findInnerRectanglePixels(self, shape) -> Rectangle:
        # find the largest interior rectangle
        topLeft_x, topLeft_y, w, h = lir(shape.pixels == 0)
        w2, h2 = shape.dim()

        # have to adjust because we consider the center of the image to be the origin
        return Rectangle.fromTopLeft(Point(topLeft_x - h2 / 2, w2 / 2 - topLeft_y), w, h)

    def findInnerRectanglePixels2(self, shape) -> Rectangle:
        # find the largest interior rectangle
        w0, h0 = shape.dim()
        xs = np.arange(start=-w0 / 2, stop=(w0 / 2) + 1, step=1)
        ys = np.arange(start=(w0 / 2), stop=(-h0 / 2) - 1, step=-1)

        x, y, w, h = lir_by_histogram(shape.pixels == 0, xs, ys)
        return Rectangle.fromTopLeft(Point(xs[x], ys[int(y)]), w, h)