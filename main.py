from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.Point import Point
from src.birectangle.Segment import Segment
from src.birectangle.innerrectanglefinder.BarycenterRectangleFinder import BarycenterRectangleFinder
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.cuttingmethod.FullHorizontalCut import FullHorizontalCut
from src.birectangle.cuttingmethod.FullSideNonDisjointCut import FullSideNonDisjointCut
from src.birectangle.cuttingmethod.FullVerticalCut import FullVerticalCut
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/simple_test.bmp")
#SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

'''
m = BiRectangleMethod(innerRectFinder=BarycenterRectangleFinder())
m = BiRectangleMethod(keep=3, biRectAnalogy=ExtSigmoidAnalogy())

shape_res = m.analogy(SA, SB, SC)
if shape_res is not None:
    shape_res.toImage()
else:
    print("no solution")
'''

barycenter = BarycenterRectangleFinder()
barycenter.findInnerRectanglePixels(SA)

'''
print(SA.isHorizontalSegmentInShape(Segment(Point(0,.3), Point(3,.3))))
'''