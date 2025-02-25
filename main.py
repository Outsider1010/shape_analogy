from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.innerrectanglefinder.BarycenterRectangleFinder import BarycenterRectangleFinder
from src.shapes.pixelShape import PixelShape

#SA = PixelShape(img="resources/simple_test.bmp")
SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_2.bmp")

m = BiRectangleMethod(innerRectFinder=BarycenterRectangleFinder())
shape_res = m.analogy(SA, SB, SC)
if shape_res is not None:
    shape_res = shape_res.resize(300, 300)
    shape_res.toImage()
else:
    print("no solution")

'''
barycenter = BarycenterRectangleFinder()
barycenter.findInnerRectanglePixels(SA)
'''