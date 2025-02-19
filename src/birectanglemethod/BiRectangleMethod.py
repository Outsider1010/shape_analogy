from src.ShapeAnalogy import ShapeAnalogy
from src.birectanglemethod.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectanglemethod.birectangle import BiRectangle
from src.birectanglemethod.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.birectanglemethod.innerrectanglefinder.LargestRectangleFinder import LargestRectangleFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape


class BiRectangleMethod(ShapeAnalogy):

    def __init__(self, BRAnalogy = SigmoidCenterAnalogy, CutMethod = FirstCuttingIn4Method,
                 InnerRectangle = LargestRectangleFinder):
        self.biRectangleAnalogy = BRAnalogy()
        self.cuttingMethod = CutMethod()
        self.innerRectangleFinder = InnerRectangle()


    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> PixelShape | None:
        shape_list = (SA, SB, SC)

        birectangles = tuple(BiRectangle(shape.getOuterRectangle(),
                                         shape.getInnerRectangle(self.innerRectangleFinder)) for shape in shape_list)
        try:
            birectangle_d = self.biRectangleAnalogy.analogy(*birectangles)
            d = PixelShape(rect=birectangle_d.innerRectangle)
        except AssertionError:
            print("No solution was found.")
            return None

        subshapes = tuple(shape_list[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))

        for i in range(self.cuttingMethod.nbSubShapes()):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]

            emptyA = subshapeA.isEmpty()
            emptyB = subshapeB.isEmpty()
            emptyC = subshapeC.isEmpty()
            if not emptyA and not emptyB and not emptyC:
                subshapeD = self.analogy(subshapeA, subshapeB, subshapeC)
                if subshapeD is None:
                    return None
                d.merge(subshapeD)
            elif emptyA and emptyB and emptyC:
                continue
            elif emptyA and emptyB:
                d.merge(subshapeC)
            elif emptyA and emptyC:
                d.merge(subshapeB)

        return d
