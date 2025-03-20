from matplotlib import pyplot as plt
from tifffile import imshow

from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.birectangle.birectangleanalogy.ext_sigmoid_analogy import ExtSigmoidAnalogy
from src.birectangle.innerrectanglefinder.barycenter_rectangle_finder import BarycenterRectangleFinder
from src.shapes.pixel_shape import PixelShape
from src.shapes.union_rectangles import UnionRectangles

SA = PixelShape(img="resources/circle_1.bmp")
SB = PixelShape(img="resources/circle_2.bmp")
SC = PixelShape(img="resources/circle_1.bmp")

m = BiRectangleMethod(algo='iter', keep=2, epsilon=0.00001, innerRectFinder=BarycenterRectangleFinder(), biRectAnalogy=ExtSigmoidAnalogy(), plot='last', maxDepth=7)
SD : UnionRectangles = m.analogy(SA, SB, SC)
print("Affiche le résultat final...")
plt.imshow(SD.toPixels(), cmap='gray', origin='lower')
print("Résultat final affiché succès !")