
from src.birectangle.birectangleanalogy.bi_rectangle_analogy import BiRectangleAnalogy
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy
from src.birectangle.rectangle import Rectangle


# TODO: documentation
class RatioAnalogy(BiRectangleAnalogy):

    def __init__(self, rectangleAnalogy = CenterDimAnalogy()):
        self.rectAnalogy = rectangleAnalogy

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        # print(BRA.center_xy_ratios(), BRB.center_xy_ratios(), BRC.center_xy_ratios(), sep='\n')
        # assert BRA.center_xy_ratios() == BRB.center_xy_ratios() == BRC.center_xy_ratios(), "To use the ratio analogy, the ratios of A, B and C should be the same"

        if not outerRectD:
            outerRectD = self.rectAnalogy.analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)

        r_x_min, r_x_max, r_y_min, r_y_max = BRA.center_xy_ratios()

        res = BiRectangle(outerRectD, outerRectD)
        res.reduceInnerTo(r_x_min, r_x_max, r_y_min, r_y_max)

        return res

