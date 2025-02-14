from src.ShapeAnalogy import ShapeAnalogy
from src.biframemethod.biframeanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.biframemethod.birectangle import BiRectangle
from src.biframemethod.cuttingmethod.FirstCuttingIn4Method import FirstCuttingIn4Method
from src.biframemethod.innerframefinder.LargestFrameFinder import LargestFrameFinder
from src.shapes.pixelShape import PixelShape
from src.shapes.shape import Shape


class BiFrameMethod(ShapeAnalogy):

    def __init__(self):
        self.biFrameAnalogy = SigmoidCenterAnalogy()
        self.cuttingMethod = FirstCuttingIn4Method()
        self.innerFrameFinder = LargestFrameFinder()


    def analogy(self, SA : Shape, SB : Shape, SC : Shape) -> Shape:
        shape_list = (SA, SB, SC)

        birectangles = tuple(BiRectangle(shape.getOuterRectangle(),
                                         shape.getInnerRectangle(self.innerFrameFinder)) for shape in shape_list)

        birectangle_d = self.biFrameAnalogy.analogy(*birectangles)

        nbSubShapes = self.cuttingMethod.nbSubShapes()
        subshapes = tuple(shape_list[i].cut(birectangles[i], self.cuttingMethod) for i in range(3))

        p = PixelShape(rect=birectangle_d.innerRectangle)

        for i in range(nbSubShapes):
            subshapeA: Shape = subshapes[0][i]
            subshapeB: Shape = subshapes[1][i]
            subshapeC: Shape = subshapes[2][i]
            # if one of the shapes is empty, we don't do anything,
            # but we could (although, we won't have rectangles as solutions)
            if not (subshapeA.isEmpty() or subshapeB.isEmpty() or subshapeC.isEmpty()):
                subshapeD = self.analogy(subshapeA, subshapeB, subshapeC)
                # TODO : à compléter, i.e fusionner p et subshapeD

            # elif subshape_a.isEmpty() and subshape_b.isEmpty() and subshape_c.isEmpty():
            #     continue
            # elif subshape_a.isEmpty() and subshape_b.isEmpty():
            #     results.append(subshape_c)
            # elif subshape_a.isEmpty() and subshape_c.isEmpty():
            #     results.append(subshape_b)
        return p
