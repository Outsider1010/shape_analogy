from src.biframemethod.BiFrameMethod import BiFrameMethod
from src.shapes.pixelShape import PixelShape
from src.utils import array_to_image

SA = PixelShape.fromImage(img="resources/square.bmp")
SB = PixelShape.fromImage(img="resources/square.bmp")
SC = PixelShape.fromImage(img="resources/square.bmp")

s = BiFrameMethod()
res = s.analogy(SA, SB, SC)
array_to_image(res.pixels)