from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/circle_4.bmp")
SB = PixelShape(img="resources/circle_1.bmp")
SC = PixelShape(img="resources/circle_3.bmp")

m = BiRectangleMethod(algo='iter', plot='step', keep=1, epsilon=0.0001)
m.analogy(SA, SB, SC)