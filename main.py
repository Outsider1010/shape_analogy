from decimal import Decimal

from matplotlib import pyplot as plt

from src.basicanalogies.realnumbers import bounded
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
from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.area_analogy import AreaAnalogy
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangleanalogy.coord_analogy import CoordAnalogy
from src.shapes.factory import ShapeFactory
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles


l = LargestRectangleFinder()

'''
SA = PixelShape(img='resources/circle_1.bmp')
SB = PixelShape(img='resources/formeIr/donut/donut3.bmp')
SC = PixelShape(img='resources/exact_rhombus.bmp')
'''

'''
SA = PixelShape(img='resources/ellipse_1.bmp')
SB = PixelShape(img='resources/e_1_-30deg.bmp')
SC = PixelShape(img='resources/e_1_-30deg.bmp')
'''

'''
SA = UnionRectangles()
SA.addRectangle(Rectangle(0., 5, 0, 1))
SA.addRectangle(Rectangle(2.25, 2.75, 1, 2))

SB = UnionRectangles()
SB.addRectangle(Rectangle(0., 5, 0, 1))
SB.addRectangle(Rectangle(1.5, 3.5, 1, 2))

SC = SB

SD = UnionRectangles()
SD.addRectangle(Rectangle(0., 5, 0, 1))
SD.addRectangle(Rectangle(0.5, 4.5, 1, 2))
'''
'''
SA = PixelShape(img='resources/circle_1.bmp').toRectangles(l)
SC = SA.fromShape(Rectangle.fromTopLeft(Point(Decimal(-33), Decimal(127)), Decimal(152), Decimal(76)))
SB = PixelShape(img='resources/exact_rhombus.bmp')
SD = SB.fromShape(Rectangle(Decimal('-59'), Decimal('59'), Decimal('10'), Decimal('78')))
'''

SA = PixelShape(img='resources/circle_1.bmp')
SB = PixelShape(img='resources/circle_2.bmp')
SC = PixelShape(img='resources/circle_3.bmp')

'''
SA = PixelShape(img='resources/ss_star.bmp')
SB = PixelShape(img='resources/ss_eclair.bmp')
SC = PixelShape(img='resources/ss_eclair2.bmp')
'''

# SA = ShapeFactory.rectangleFromBottomLeft(Point(Decimal('0'), Decimal('0')), 4, 1)
m = BiRectangleMethod(biRectAnalogy =ExtSigmoidAnalogy(), cutMethod = CutIn4EqualParts1(),
                      maxDepth = 7, nbIterations = 1500, overflowPrevention = IndirectPrevention(),
                      subSys = 'cut', algo  = 'rec', sameAxis = False, plot='step')

d = m.analogy(SA, SB, SC)
r = m.analogy(SC, d, SA)
