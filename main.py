import math
import time

import matplotlib.pyplot as plt
import numpy as np

from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.birectangleanalogy.simple_analogy import SimpleAnalogy
from src.birectangle.innerrectanglefinder.largest_rectangle_finder import LargestRectangleFinder
from src.birectangle.rectangle import Rectangle
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/circle_1.bmp")
SB = PixelShape(img="resources/circle_2.bmp")
SC = PixelShape(img="resources/circle_1.bmp")
l = LargestRectangleFinder()

SA.toSinogram()

m = BiRectangleMethod(algo='rec', keep=2)
d = m.analogy(SA, SB, SC)
d2 = time.time()
d.toImage('M1')
print(time.time() - d2)

#251.70357656478882
#0.0948324203491211
