from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

m = BiRectangleMethod(plot=3)
shape_res = m.analogy(SA, SB, SC)
if shape_res is not None:
    shape_res = shape_res.resize(300, 300)
    shape_res.toImage()
else:
    print("no solution")