from src.basicanalogies.realnumbers import bounded, ext_bounded
from src.birectangle.BiRectangle import BiRectangle
from src.birectangle.Point import Point
from src.birectangle.Rectangle import Rectangle
from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.rectangleanalogy.CenterDimAnalogy import CenterDimAnalogy


class ExtSigmoidAnalogy(BiRectangleAnalogy):

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        outerD = CenterDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        wOuterD = outerD.width()
        hOuterD = outerD.height()

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
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA_inner_center.x - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        xB_rescale = (BRB_inner_center.x - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        xC_rescale = (BRC_inner_center.x - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()
        xD_rescale = ext_bounded(xA_rescale, xB_rescale, xC_rescale, (wA_rescale / 2, 1 - wA_rescale / 2),
                                 (wB_rescale / 2, 1 - wB_rescale / 2), (wC_rescale / 2, 1 - wC_rescale / 2),
                                 (wD_rescale / 2, 1 - wD_rescale / 2))
        xD = outerD.x_min + wOuterD * xD_rescale

        yA_rescale = (- BRA_inner_center.y + BRA.outerRectangle.y_max) / BRA.outerRectangle.height()
        yB_rescale = (- BRB_inner_center.y + BRB.outerRectangle.y_max) / BRB.outerRectangle.height()
        yC_rescale = (- BRC_inner_center.y + BRC.outerRectangle.y_max) / BRC.outerRectangle.height()
        yD_rescale = ext_bounded(yA_rescale, yB_rescale, yC_rescale, (hA_rescale / 2, 1 - hA_rescale / 2),
                                 (hB_rescale / 2, 1 - hB_rescale / 2), (hC_rescale / 2, 1 - hC_rescale / 2),
                                 (hD_rescale / 2, 1 - hD_rescale / 2))
        yD = outerD.y_max - hOuterD * yD_rescale

        innerD = Rectangle.fromCenter(Point(xD, yD), wD, hD)

        return BiRectangle(outerD, innerD)