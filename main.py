<<<<<<< HEAD
from src.ShapeAnalogyApp import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
=======
from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.birectangleanalogy.ExtSigmoidAnalogy import ExtSigmoidAnalogy
from src.shapes.pixelShape import PixelShape

SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")


m = BiRectangleMethod(keep=3, plot='step', biRectAnalogy=ExtSigmoidAnalogy())
shape_res = m.analogy(SA, SB, SC)
if shape_res is not None:
    shape_res.toImage()
else:
    print("no solution")
>>>>>>> main
