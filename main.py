from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixelShape import PixelShape
from src.utils import resize, toImage
from src.birectangle.birectangleanalogy.SigmoidCenterAnalogy import SigmoidCenterAnalogy
from src.birectangle.birectangleanalogy.SigmoidTopLeftAnalogy import SigmoidTopLeftAnalogy
import time

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

m = BiRectangleMethod(BiRectAnalogy=SigmoidCenterAnalogy())
d = time.time()
shape_res, full_array = m.analogy(SA, SB, SC)
print(time.time() - d)
if full_array is not None:
    arr = resize(full_array, 300, 300)
    toImage(arr)
else:
    print("no solution")