from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape
from src.utils import toImage, resize2D
from src.birectangle.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectangle.birectangleanalogy.CornerAnalogy import CornerAnalogy

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

m = BiRectangleMethod(BRAnalogy=SigmoidCenterAnalogy())
shape_res, full_array = m.analogy(SA, SB, SC)
if full_array is not None:
    arr = resize2D(full_array, 300, 300)
    toImage(arr)
else:
    print("no solution")