from src.birectangle.bi_rectangle_method import BiRectangleMethod
from src.shapes.pixel_shape import PixelShape

SA = PixelShape(img="resources/circle_1.bmp")
SB = PixelShape(img="resources/circle_2.bmp")
SC = PixelShape(img="resources/circle_1.bmp")

m = BiRectangleMethod(algo='rec', keep=2, epsilon=0.001, maxDepth=10)
m.analogy(SA, SB, SC)