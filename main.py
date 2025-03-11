from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.Point import Point
from src.birectangle.Rectangle import Rectangle
from src.birectangle.birectangleanalogy.BiSegmentAnalogy import BiSegmentAnalogy
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.birectangle.cuttingmethod.CuttingIn8 import CuttingIn8
from src.birectangle.cuttingmethod.CutIn4EqualParts1 import CutIn4EqualParts1
from src.birectangle.cuttingmethod.HorizontalCut import HorizontalCut
from src.birectangle.cuttingmethod.SidesNonDisjointCut import SidesNonDisjointCut
from src.birectangle.cuttingmethod.VerticalCut import VerticalCut
from src.birectangle.rectangleanalogy.CoordAnalogy import CoordAnalogy
from src.birectangle.rectangleanalogy.TopLeftDimAnalogy import TopLeftDimAnalogy
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

# m = BiRectangleMethod(keep=0, plot='step', epsilon=0.01, maxDepth=12,
#                       cutMethod=CutIn4EqualParts1(), biRectAnalogy=ExtSigmoidAnalogy())
#
# shape_res = m.analogy(SA, SB, SC).resize(300, 300)
# shape_res.toImage("abc_1.bmp")

# m = BiRectangleMethod(keep=1, plot='step', epsilon=0.01, maxDepth=12,
#                       cutMethod=SidesNonDisjointCut(), biRectAnalogy=BiSegmentAnalogy())
#
# shape_res = m.analogy(SA, SB, SC).resize(300, 300)
# shape_res.toImage("abc_2.bmp")

# m = BiRectangleMethod(keep=2, plot='step', epsilon=0.01, maxDepth=12, innerReduction=True, ratioAnalogy=True,
#                       cutMethod=SidesNonDisjointCut(), biRectAnalogy=ExtSigmoidAnalogy())
#
# shape_res = m.analogy(SA, SB, SC).resize(300, 300)
# shape_res.toImage("abc_3.bmp")

