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


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, BRAnalogy = ExtSigmoidAnalogy, CutMethod = FirstCuttingIn4Method,
                 InnerRectangle = LargestRectangleFinder, epsilon = 0.1, maxIteration = 3000):
        assert epsilon < 0.5, f"Epsilon value ({epsilon}) is too high (should be < 0.5)"
        self.biRectangleAnalogy = BRAnalogy()
        self.cuttingMethod = CutMethod()
        self.innerRectangleFinder = InnerRectangle()
        self.epsilon = epsilon
        self.maxIteration = maxIteration

    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> tuple[PixelShape | Shape | None, np.ndarray | None]:
        # list of regions where no subshape could be obtained (unsolvable equations)
        unresolved: list[Rectangle] = []
        res = self.__analogy(SA, SB, SC, self.maxIteration, unresolved)
        if res is not None:
            h, w = res.dim()
            full_array = np.ones((h, w), dtype=np.uint8) * 255
            full_array[res.pixels] = np.uint8(0)
            for r in unresolved:
                tmp = full_array[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
                                 int(r.x_min + w / 2): ceil(r.x_max + w / 2)]
                full_array[int(h / 2 - r.y_max): ceil(h / 2 - r.y_min),
                           int(r.x_min + w / 2): ceil(r.x_max + w / 2)] = np.maximum(tmp, np.uint8(127))
            return res, full_array
        else:
            return None, None

    def __analogy(self, SA : Shape, SB : Shape, SC : Shape, k, unresolved) -> PixelShape | Shape | None:
        emptyA = SA.isEmpty()
        emptyB = SB.isEmpty()
        emptyC = SC.isEmpty()
        # base cases
        if emptyA and emptyB:
            return SC
        elif emptyA and emptyC:
            return SB
        # unsolvable equations with empty shapes
        elif emptyA or emptyB or emptyC:
            lgg.warning(" Unsolvable equation with empty shape. Analogy unsolved.")
            return None

        shapes = (SA, SB, SC)
        birectangles = tuple(BiRectangle(s.getOuterRectangle(),
                                         s.getInnerRectangle(self.innerRectangleFinder)) for s in shapes)

        # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
        for biRect in birectangles:
            biRect.separate(self.epsilon)

        try:
            birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
        except AssertionError as e:
            lgg.warning(f" {e}. Analogy unsolved.")
            return None

        d = PixelShape(rect=birectangle_d.innerRectangle)

        subshapes = tuple(shapes[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))
        nbSubShapes = self.cuttingMethod.nbSubShapes()
        for i in range(nbSubShapes):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]
            if k > 0:
                subshapeD = self.__analogy(subshapeA, subshapeB, subshapeC, k // nbSubShapes, unresolved)
                if subshapeD is not None:
                    d = d + subshapeD
                else:
                    unresolved.append(self.cuttingMethod.cutBiRectangle(birectangle_d)[i])
        return d
