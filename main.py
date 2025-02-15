from src.biframemethod.BiFrameMethod import BiFrameMethod
from src.biframemethod.innerframefinder.BarycenterFrameFinder import BarycenterFrameFinder
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/square.bmp")
SB = PixelShape(img="resources/square_ul.bmp")
SC = PixelShape(img="resources/square.bmp")

# s = BiFrameMethod()
# res = s.analogy(SA, SB, SC)
# res.toImage()

f = BarycenterFrameFinder().findInnerFramePixels(PixelShape(img="resources/simple_test.bmp"))
print(f)