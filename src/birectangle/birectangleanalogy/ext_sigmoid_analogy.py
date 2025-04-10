from src.basicanalogies.realnumbers import bounded, ext_bounded
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.point import Point
from src.birectangle.rectangle import Rectangle
from src.birectangle.birectangleanalogy.bi_rectangle_analogy import BiRectangleAnalogy
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy


# TODO: documentation
class ExtSigmoidAnalogy(BiRectangleAnalogy):

    def __init__(self, rectangleAnalogy = CenterDimAnalogy()):
        self.rectAnalogy = rectangleAnalogy

    """
    A method to solve analogical equations on some birectangles.
    Birectangles where the inner rectangle does not touch the outer rectangle.
    """
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        if not outerRectD:
            outerRectD = CenterDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        wOuterD = outerRectD.width()
        hOuterD = outerRectD.height()

        wA_rescale = BRA.innerRectangle.width() / BRA.outerRectangle.width()
        wB_rescale = BRB.innerRectangle.width() / BRB.outerRectangle.width()
        wC_rescale = BRC.innerRectangle.width() / BRC.outerRectangle.width()
        wD_rescale = bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = wOuterD * wD_rescale

        hA_rescale = BRA.innerRectangle.height() / BRA.outerRectangle.height()
        hB_rescale = BRB.innerRectangle.height() / BRB.outerRectangle.height()
        hC_rescale = BRC.innerRectangle.height() / BRC.outerRectangle.height()
        hD_rescale = bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = hOuterD * hD_rescale

        BRA_inner_center = BRA.innerRectangle.center()
        BRB_inner_center = BRB.innerRectangle.center()
        BRC_inner_center = BRC.innerRectangle.center()

        xA_rescale = (BRA_inner_center.x - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        xB_rescale = (BRB_inner_center.x - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        xC_rescale = (BRC_inner_center.x - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()
        xD_rescale = ext_bounded(xA_rescale, xB_rescale, xC_rescale, (wA_rescale / 2, 1 - wA_rescale / 2),
                                 (wB_rescale / 2, 1 - wB_rescale / 2), (wC_rescale / 2, 1 - wC_rescale / 2),
                                 (wD_rescale / 2, 1 - wD_rescale / 2))
        xD = outerRectD.x_min + wOuterD * xD_rescale

        yA_rescale = (- BRA_inner_center.y + BRA.outerRectangle.y_max) / BRA.outerRectangle.height()
        yB_rescale = (- BRB_inner_center.y + BRB.outerRectangle.y_max) / BRB.outerRectangle.height()
        yC_rescale = (- BRC_inner_center.y + BRC.outerRectangle.y_max) / BRC.outerRectangle.height()
        yD_rescale = ext_bounded(yA_rescale, yB_rescale, yC_rescale, (hA_rescale / 2, 1 - hA_rescale / 2),
                                 (hB_rescale / 2, 1 - hB_rescale / 2), (hC_rescale / 2, 1 - hC_rescale / 2),
                                 (hD_rescale / 2, 1 - hD_rescale / 2))
        yD = outerRectD.y_max - hOuterD * yD_rescale

        innerD = Rectangle.fromCenter(Point(xD, yD), wD, hD)
        return BiRectangle(outerRectD, innerD)