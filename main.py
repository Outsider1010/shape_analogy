<<<<<<< HEAD
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.birectanglemethod.BiRectangleMethod import BiRectangleMethod
=======
from src.birectangle.BiRectangleMethod import BiRectangleMethod
from src.birectangle.birectangleanalogy.SigmoidTopLeftAnalogy import SigmoidTopLeftAnalogy
>>>>>>> main
from src.shapes.pixelShape import PixelShape
from src.ShapeAnalogyApp import App



app = App()
"""SA = PixelShape(img="resources/ellipse_1.bmp")
SB = PixelShape(img="resources/ellipse_2.bmp")
SC = PixelShape(img="resources/ellipse_3.bmp")

<<<<<<< HEAD
res = BiRectangleMethod().analogy(SA, SB, SC)
if res:
    res.toImage()"""
=======
res = BiRectangleMethod(BRAnalogy= SigmoidTopLeftAnalogy).analogy(SA, SB, SC)
if res is not None:
    res.toImage()
else:
    print("no solution")
>>>>>>> main
