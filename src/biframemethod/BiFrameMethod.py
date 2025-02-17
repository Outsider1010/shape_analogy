from src.ShapeAnalogy import ShapeAnalogy
from src.biframemethod.biframeanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.biframemethod.innerframefinder.LargestFrameFinder import LargestFrameFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape


class BiFrameMethod(ShapeAnalogy):

    def __init__(self, BFAnalogy = SigmoidCenterAnalogy, CutMethod = FirstCuttingIn4Method,
                 InnerFrame = LargestFrameFinder):
        self.biFrameAnalogy = BFAnalogy()
        self.cuttingMethod = CutMethod()
        self.innerFrameFinder = InnerFrame()


    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> PixelShape:
        shape_list = (SA, SB, SC)

        birectangles = tuple(BiRectangle(shape.getOuterFrame(),
                                         shape.getInnerFrame(self.innerFrameFinder)) for shape in shape_list)

        birectangle_d = self.biFrameAnalogy.analogy(*birectangles)
        d: PixelShape = PixelShape(rect=birectangle_d.innerRectangle)

        subshapes = tuple(shape_list[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))

        for i in range(self.cuttingMethod.nbSubShapes()):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]
            if not (subshapeA.isEmpty() or subshapeB.isEmpty() or subshapeC.isEmpty()):
                subshapeD = self.analogy(subshapeA, subshapeB, subshapeC)
                d.merge(subshapeD)
            elif subshapeA.isEmpty() and subshapeB.isEmpty() and subshapeC.isEmpty():
                continue
            elif subshapeA.isEmpty() and subshapeB.isEmpty():
                d.merge(subshapeC)
            elif subshapeA.isEmpty() and subshapeC.isEmpty():
                d.merge(subshapeB)

        return d
