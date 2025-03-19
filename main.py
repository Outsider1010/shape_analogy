from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/square.bmp")
SB = PixelShape(img="resources/square.bmp")
SC = PixelShape(img="resources/square.bmp")

m = BiRectangleMethod()
m.analogy2(SA, SB, SC)