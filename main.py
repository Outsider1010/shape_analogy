from matplotlib import pyplot as plt
from tifffile import imshow

from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.bi_segment_analogy import BiSegmentAnalogy
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.birectangleanalogy.ratio_analogy import RatioAnalogy
from src.birectangle.innerrectanglefinder.barycenter_rectangle_finder import BarycenterRectangleFinder
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/weird_shape.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

m = BiRectangleMethod(algo='iter', keep=4,innerReduction = True, biRectAnalogy=RatioAnalogy(), epsilon=0.00001, plot='last', maxDepth=8)
SD : UnionRectangles = m.analogy(SA, SB, SC)