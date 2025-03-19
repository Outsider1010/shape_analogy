from numpy.ma.core import inner

from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.basicanalogies.realnumbers import bounded
from src.birectangle.rectangleanalogy.CenterDimAnalogy import CenterDimAnalogy
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point


# TODO: documentation
class SimpleAnalogy(BiRectangleAnalogy):

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        if not outerRectD:
            outerRectD = CenterDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        _innerD = CenterDimAnalogy().analogy(BRA.innerRectangle, BRB.innerRectangle, BRC.innerRectangle)

        x_min = max(_innerD.x_min, outerRectD.x_min)
        x_max = min(_innerD.x_max, outerRectD.x_max)
        y_min = max(_innerD.y_min, outerRectD.y_min)
        y_max = min(_innerD.y_max, outerRectD.y_max)
        if x_max - x_min > 0 and y_max - y_min > 0:
            return BiRectangle(outerRectD, Rectangle(x_min, x_max, y_min, y_max))
        else:
            raise AssertionError('no solution found')

