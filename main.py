from src.birectanglemethod.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

res = BiRectangleMethod().analogy(SA, SB, SC)
if res:
    res.toImage()