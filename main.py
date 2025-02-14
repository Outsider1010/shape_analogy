from src.biframemethod.BiFrameMethod import BiFrameMethod
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/square.bmp")
SB = PixelShape(img="resources/square.bmp")
SC = PixelShape(img="resources/square.bmp")

s = BiFrameMethod()
res = s.analogy(SA, SB, SC)
res.toImage()