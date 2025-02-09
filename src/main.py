from shapes.pixelShape import PixelShape
from src.birectangle import BiRectangle
from src.shapes.shape import Shape
from src.utils import visualize

SA = PixelShape(img="resources/square.bmp")
SB = PixelShape(img="resources/square.bmp")
SC = PixelShape(img="resources/square.bmp")

res = Shape.analogy(SA, SB, SC, birectAnalogy=BiRectangle.analogy_center)
visualize(res)