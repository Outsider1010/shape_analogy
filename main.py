from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.birectangleanalogy.SigmoidTopLeftAnalogy import SigmoidTopLeftAnalogy
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

res = BiRectangleMethod(BRAnalogy= SigmoidTopLeftAnalogy).analogy(SA, SB, SC)
if res is not None:
    res.toImage()
else:
    print("no solution")