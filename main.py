from decimal import Decimal

from matplotlib import pyplot as plt

from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.birectangleanalogy.simple_analogy import SimpleAnalogy
from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.cuttingmethod.cut_in_8 import CuttingIn8
from src.birectangle.cuttingmethod.horizontal_cut import HorizontalCut
from src.birectangle.cuttingmethod.sides_non_disjoint_cut import SidesNonDisjointCut
from src.birectangle.cuttingmethod.vertical_cut import VerticalCut
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.overflowprevention.direct_prevention import DirectPrevention
from src.birectangle.overflowprevention.indirect_prevention import IndirectPrevention
from src.birectangle.overflowprevention.no_prevention import NoPrevention
from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.area_analogy import AreaAnalogy
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangleanalogy.coord_analogy import CoordAnalogy
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles


l = LargestRectangleFinder()

SA = PixelShape(img='resources/ellipse_1.bmp')
SB = PixelShape(img='resources/ellipse_2.bmp')
SC = PixelShape(img='resources/ellipse_3.bmp')

m = BiRectangleMethod(biRectAnalogy = BiSegmentAnalogy(), cutMethod = HorizontalCut(),
                      maxDepth = 6, nbIterations = 2000, epsilon = 0.0001, overflowPrevention = IndirectPrevention(epsilon=0.0001),
                      subSys = 'super', algo  = 'rec', sameAxis = False, plot='step')

d = m.analogy(SA, SB, SC)
m.analogy(SC, d, SA)