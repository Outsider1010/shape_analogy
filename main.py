from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.birectangleanalogy.ratio_analogy import RatioAnalogy
from src.birectangle.birectangleanalogy.simple_analogy import SimpleAnalogy
from src.birectangle.cuttingmethod.cut_in_4_equal_parts_1 import CutIn4EqualParts1
from src.birectangle.cuttingmethod.vertical_cut import VerticalCut
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.overflowprevention.direct_prevention import DirectPrevention
from src.birectangle.overflowprevention.indirect_prevention import IndirectPrevention
from src.birectangle.overflowprevention.no_prevention import NoPrevention
from src.birectangle.rectangle import Rectangle
from src.birectangle.rectangleanalogy.coord_analogy import CoordAnalogy
from src.shapes.pixel_shape import PixelShape


SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")
l = LargestRectangleFinder()

m = BiRectangleMethod(biRectAnalogy = BiSegmentAnalogy(), cutMethod = CutIn4EqualParts1(),
                      maxDepth = 6, nbIterations = 1365, epsilon = 0.001, overflowPrevention  = DirectPrevention(),
                      subSys = 'cut', innerReduction = False, algo  = 'iter', sameAxis = False, plot='step')
d = m.analogy(SA, SB, SC)
d.toImage('test')