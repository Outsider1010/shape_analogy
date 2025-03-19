
from src.birectangle.birectangleanalogy.bi_rectangle_analogy import BiRectangleAnalogy
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangle import Rectangle


# TODO: documentation
class SimpleAnalogy(BiRectangleAnalogy):

    def __init__(self, rectangleAnalogy = CenterDimAnalogy()):
        self.rectAnalogy = rectangleAnalogy

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        if not outerRectD:
            outerRectD = self.rectAnalogy.analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        _innerD = self.rectAnalogy.analogy(BRA.innerRectangle, BRB.innerRectangle, BRC.innerRectangle)

        x_min = max(_innerD.x_min, outerRectD.x_min)
        x_max = min(_innerD.x_max, outerRectD.x_max)
        y_min = max(_innerD.y_min, outerRectD.y_min)
        y_max = min(_innerD.y_max, outerRectD.y_max)
        if x_max - x_min > 0 and y_max - y_min > 0:
            return BiRectangle(outerRectD, Rectangle(x_min, x_max, y_min, y_max))
        else:
            raise AssertionError('no solution found')

