from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.overflowprevention.direct_prevention import DirectPrevention
from src.birectangle.overflowprevention.indirect_prevention import IndirectPrevention
from src.birectangle.overflowprevention.no_prevention import NoPrevention
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/circle_4.bmp")
SB = PixelShape(img="resources/circle_1.bmp")
SC = PixelShape(img="resources/circle_3.bmp")
l = LargestRectangleFinder()

m = BiRectangleMethod(algo='iter', plot='step', overflowPrevention=DirectPrevention(), subSys='cut',
                      epsilon=0.0001, biRectAnalogy=BiSegmentAnalogy())
d = m.analogy(SA, SB, SC)
