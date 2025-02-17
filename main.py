from src.biframemethod.BiFrameMethod import BiFrameMethod
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/square.bmp")
SB = PixelShape(img="resources/square_ul.bmp")
SC = PixelShape(img="resources/square.bmp")

res = BiFrameMethod().analogy(SA, SB, SC)
res.toImage()