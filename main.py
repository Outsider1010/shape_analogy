from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/circle_1.bmp")
SB = PixelShape(img="resources/circle_2.bmp")
SC = PixelShape(img="resources/circle_3.bmp")

m = BiRectangleMethod()
m.analogy2(SA, SB, SC)