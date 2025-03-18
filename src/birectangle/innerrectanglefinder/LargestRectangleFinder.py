from decimal import Decimal

import numpy as np
from largestinteriorrectangle import lir

from src.birectangle.innerrectanglefinder.InnerRectangleFinder import InnerRectangleFinder
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point
from src.shapes.UnionRectangles import UnionRectangles


class LargestRectangleFinder(InnerRectangleFinder):
    """
    Find the largest interior axis aligned rectangle of a shape.
    """

    def findInnerRectangleUnionR(self, shape: UnionRectangles) -> Rectangle:
        xs = set()
        ys = set()
        for r in shape.rectangles:
            xs.add(r.x_min)
            xs.add(r.x_max)
            ys.add(r.y_min)
            ys.add(r.y_max)
        xs = sorted(xs)
        ys = sorted(ys)
        matrix = np.zeros((len(ys) - 1, len(xs) - 1), dtype=bool)

        for r in shape.rectangles:
            i_x_min = i_y_min = np.inf
            i_x_max = i_y_max = -np.inf
            for i in range(len(xs)):
                if xs[i] == r.x_min:
                    i_x_min = i
                if xs[i] == r.x_max:
                    i_x_max = i
            for i in range(len(ys)):
                if ys[i] == r.y_min:
                    i_y_min = i
                if ys[i] == r.y_max:
                    i_y_max = i
            matrix[i_y_min:i_y_max, i_x_min:i_x_max] = True
        h_adj = np.zeros_like(matrix, dtype=int)
        v_adj = np.zeros_like(matrix, dtype=int)

        h_adj[:,-1] = matrix[:,-1]
        for i in range(matrix.shape[1] - 2, -1, -1):
            h_adj[:,i] = matrix[:,i] + matrix[:, i] * h_adj[:, i+1]

        v_adj[-1, :] = matrix[-1, :]
        for i in range(matrix.shape[0] - 2, -1, -1):
            v_adj[i, :] = matrix[i,:] + matrix[i,:] * v_adj[i+1, :]

        x = y = w = h = 0
        best_area = 0
        cy, cx = np.where(matrix)
        for k in range(cy.shape[0]):
            i = cy[k]
            j = cx[k]
            _w1 = h_adj[i, j]
            _h2 = v_adj[i, j]
            j1 = j + _w1 - 1
            i2 = i + _h2 - 1
            _h1 = min(v_adj[i, j1], _h2)
            _w2 = min(h_adj[i2, j], _w1)
            area1 = (ys[i + _h1] - ys[i]) * (xs[j1 + 1] - xs[j])
            area2 = (ys[i2 + 1] - ys[i]) * (xs[j + _w2] - xs[j])
            if area1 > best_area:
                x = xs[j]
                y = ys[i]
                w = xs[j1 + 1] - xs[j]
                h = ys[i + _h1] - ys[i]
                best_area = area1
            if area2 > best_area:
                x = xs[j]
                y = ys[i]
                w = xs[j + _w2] - xs[j]
                h = ys[i2 + 1] - ys[i]
                best_area = area2
        return Rectangle.fromTopLeft(Point(Decimal(str(x)), Decimal(str(h + y))), w, h)

    def findInnerRectanglePixels(self, shape) -> Rectangle:
        # find the largest interior rectangle
        topLeft_x, topLeft_y, w, h = lir(shape.pixels)
        w2, h2 = shape.dim()

        # have to adjust because we consider the center of the image to be the origin
        return Rectangle.fromTopLeft(Point(topLeft_x - h2 / 2, w2 / 2 - topLeft_y), w, h)