from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

res = BiRectangleMethod().analogy(SA, SB, SC)
if res is not None:
    res.resize(300, 300)
    res.toImage()
else:
    print("no solution")