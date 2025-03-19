from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/circle_4.bmp")
SB = PixelShape(img="resources/circle_1.bmp")
SC = PixelShape(img="resources/circle_3.bmp")

m = BiRectangleMethod()
m.analogy(SA, SB, SC)