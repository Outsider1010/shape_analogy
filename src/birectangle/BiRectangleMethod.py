from math import ceil

import numpy as np
import logging as lgg

from src.ShapeAnalogy import ShapeAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Rectangle import Rectangle
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape
from src.utils import BLACK, RED, BLUE, GREEN, GRAY


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, BiRectAnalogy = ExtSigmoidAnalogy(), CutMethod = FirstCuttingIn4Method(),
                 InnerRectangleFinder = LargestRectangleFinder(), epsilon = 0.1, maxDepth = 7, saveSteps = False):
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        self.biRectangleAnalogy = BiRectAnalogy
        self.cuttingMethod = CutMethod
        self.innerRectangleFinder = InnerRectangleFinder
        self.epsilon = epsilon
        self.maxDepth = maxDepth

    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> tuple[PixelShape | None, np.ndarray | None]:
        # list of regions where no subshape could be obtained (unsolvable equations)
        unresolved: list[Rectangle] = []
        res = self.__analogy(SA, SB, SC, 0, unresolved)
        if res is not None:
            return res, self.__resWithUnresolved(res, unresolved)
        else:
            return None, None

    def __resWithUnresolved(self, res, unresolved):
        # grayscale shape with unresolved areas
        h, w = res.dim()
        full_array = np.ones((h, w), dtype=np.uint8) * 255
        full_array[res.pixels] = np.uint8(0)
        for r in unresolved:
            tmp = full_array[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
                  int(r.x_min + w / 2): ceil(r.x_max + w / 2)]
            full_array[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
            int(r.x_min + w / 2): ceil(r.x_max + w / 2)] = np.maximum(tmp, np.uint8(127))
        return full_array

    def __analogy(self, SA : Shape, SB : Shape, SC : Shape, k, unresolved) -> PixelShape | None:
        """
        Main analogy function
        :param SA: the shape A (first shape)
        :param SB: the shape B (second shape)
        :param SC: the shape C (third shape)
        :param k: the current depth
        :param unresolved: a list of rectangles where the analogy could not be solved
        :return: A shape D or None if the analogy could not be solved
        """
        emptyA = SA.isEmpty()
        emptyB = SB.isEmpty()
        emptyC = SC.isEmpty()

        shapes = (SA, SB, SC)

        pixelA: PixelShape = SA.toPixelShape()
        pixelB: PixelShape = SB.toPixelShape()
        pixelC: PixelShape = SC.toPixelShape()
        annotatedA = np.full((pixelA.height(), pixelA.width(), 3), 255, dtype=np.uint8)
        annotatedA[pixelA.pixels] = BLACK
        annotatedB = np.full((pixelB.height(), pixelB.width(), 3), 255, dtype=np.uint8)
        annotatedB[pixelB.pixels] = BLACK
        annotatedC = np.full((pixelC.height(), pixelC.width(), 3), 255, dtype=np.uint8)
        annotatedC[pixelC.pixels] = BLACK
        annotatedShapes = [annotatedA, annotatedB, annotatedC]

        # base cases
        if emptyA and emptyB:
            annotatedShapes.append(annotatedC)
            return pixelC
        elif emptyA and emptyC:
            annotatedShapes.append(annotatedB)
            return pixelB
        # unsolvable equations with empty shapes
        elif emptyA or emptyB or emptyC:
            lgg.warning(" Unsolvable equation with empty shape. Analogy unsolved.")
            return None

        birectangles = tuple(BiRectangle(s.getOuterRectangle(), s.getInnerRectangle(self.innerRectangleFinder)) for s in shapes)

        for i in range(3):
            # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
            birectangles[i].separate(self.epsilon)
            birectangles[i].outerRectangle.drawOnImage(annotatedShapes[i], RED)
            birectangles[i].innerRectangle.drawOnImage(annotatedShapes[i], BLUE)
            self.cuttingMethod.drawCuttingLines(birectangles[i], annotatedShapes[i], GREEN)

        try:
            birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
        except AssertionError as e:
            lgg.warning(f" {e}. Analogy unsolved.")
            return None

        # create a matrix big enough so that the outerRectangle can be drawn on it
        outerD = birectangle_d.outerRectangle
        h = ceil(max(2 * abs(outerD.y_min), 2 * abs(outerD.y_max)))
        w = ceil(max(2 * abs(outerD.x_max), 2 * abs(outerD.x_min)))
        d = PixelShape(rect=birectangle_d.innerRectangle, min_w=w, min_h=h)

        subshapes = tuple(shapes[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))
        nbSubShapes = self.cuttingMethod.nbSubShapes()
        for i in range(nbSubShapes):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]
            if k < self.maxDepth:
                subshapeD = self.__analogy(subshapeA, subshapeB, subshapeC, k + 1, unresolved)
                if subshapeD is not None:
                    d = d + subshapeD
                else:
                    unresolved.append(self.cuttingMethod.cutBiRectangle(birectangle_d)[i])

        h, w = d.dim()
        annotatedD = np.full((h, w, 3), 255, dtype=np.uint8)
        annotatedD[d.pixels] = BLACK
        birectangle_d.outerRectangle.drawOnImage(annotatedD, RED)
        birectangle_d.innerRectangle.drawOnImage(annotatedD, BLUE)
        self.cuttingMethod.drawCuttingLines(birectangle_d, annotatedD, GREEN)
        for r in unresolved:
            tmp = annotatedD[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
                  int(r.x_min + w / 2): ceil(r.x_max + w / 2)]
            annotatedD[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
            int(r.x_min + w / 2): ceil(r.x_max + w / 2)] = np.maximum(tmp, GRAY)

        annotatedShapes.append(annotatedD)
        return d
