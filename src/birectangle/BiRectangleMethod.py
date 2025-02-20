from src.ShapeAnalogy import ShapeAnalogy
from src.birectangle.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectangle.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, BRAnalogy = SigmoidCenterAnalogy, CutMethod = FirstCuttingIn4Method,
                 InnerRectangle = LargestRectangleFinder, epsilon = 1e-1, maxIteration = 100):
        self.biRectangleAnalogy = BRAnalogy()
        self.cuttingMethod = CutMethod()
        self.innerRectangleFinder = InnerRectangle()
        self.epsilon = epsilon
        self.maxIteration = maxIteration


    def analogy(self, SA : Shape, SB : Shape, SC : Shape, k = 0) -> PixelShape | Shape | None:
        emptyA = SA.isEmpty()
        emptyB = SB.isEmpty()
        emptyC = SC.isEmpty()
        # base cases
        if emptyA and emptyB:
            return SC
        elif emptyA and emptyC:
            return SB
        # not solvable equations with empty shapes
        elif emptyA or emptyB or emptyC:
            return None

        shape_list = (SA, SB, SC)
        birectangles = tuple(BiRectangle(shape.getOuterRectangle(),
                                         shape.getInnerRectangle(self.innerRectangleFinder)) for shape in shape_list)

        # prevents the inner rectangle from touching the outerRectangle (if epsilon > 0)
        for biRect in birectangles:
            if biRect.innerRectangle.x_min == biRect.outerRectangle.x_min:
                biRect.innerRectangle.x_min += self.epsilon
            if biRect.innerRectangle.x_max == biRect.outerRectangle.x_max:
                biRect.innerRectangle.x_max -= self.epsilon
            if biRect.innerRectangle.y_min == biRect.outerRectangle.y_min:
                biRect.innerRectangle.y_min += self.epsilon
            if biRect.innerRectangle.y_max == biRect.outerRectangle.y_max:
                biRect.innerRectangle.y_max -= self.epsilon

        birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
        d = PixelShape(rect=birectangle_d.innerRectangle)

        subshapes = tuple(shape_list[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))

        for i in range(self.cuttingMethod.nbSubShapes()):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]

            if k < self.maxIteration:
                subshapeD = self.analogy(subshapeA, subshapeB, subshapeC, k+1)
                if subshapeD is not None:
                    d.merge(subshapeD)

        return d
