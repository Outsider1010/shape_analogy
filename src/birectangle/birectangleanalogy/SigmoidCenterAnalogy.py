from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.basicanalogies.realnumbers import bounded
from src.birectangle.rectangleanalogy.CenterDimAnalogy import CenterDimAnalogy
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point


class SigmoidCenterAnalogy(BiRectangleAnalogy):

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        outerD = CenterDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        wOuterD = outerD.width()
        hOuterD = outerD.height()

        BRA_inner_center = BRA.innerRectangle.center()
        BRB_inner_center = BRB.innerRectangle.center()
        BRC_inner_center = BRC.innerRectangle.center()
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA_inner_center.x - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        xB_rescale = (BRB_inner_center.x - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        xC_rescale = (BRC_inner_center.x - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()
        xD_rescale = bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerD.x_min + wOuterD * xD_rescale

        yA_rescale = (- BRA_inner_center.y + BRA.outerRectangle.y_max) / BRA.outerRectangle.height()
        yB_rescale = (- BRB_inner_center.y + BRB.outerRectangle.y_max) / BRB.outerRectangle.height()
        yC_rescale = (- BRC_inner_center.y + BRC.outerRectangle.y_max) / BRC.outerRectangle.height()
        yD_rescale = bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerD.y_max - hOuterD * yD_rescale

        wA_rescale = BRA.innerRectangle.width() / BRA.outerRectangle.width()
        wB_rescale = BRB.innerRectangle.width() / BRB.outerRectangle.width()
        wC_rescale = BRC.innerRectangle.width() / BRC.outerRectangle.width()

        # if-elif added
        if wA_rescale == wC_rescale:
            wD_rescale = wB_rescale
        elif wA_rescale == wB_rescale:
            wD_rescale = wC_rescale
        elif wA_rescale == wC_rescale:
            wD_rescale = wB_rescale
        else:
            wD_rescale = bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = wOuterD * wD_rescale

        hA_rescale = BRA.innerRectangle.height() / BRA.outerRectangle.height()
        hB_rescale = BRB.innerRectangle.height() / BRB.outerRectangle.height()
        hC_rescale = BRC.innerRectangle.height() / BRC.outerRectangle.height()

        # if-elif added
        if hA_rescale == hC_rescale:
            hD_rescale = hB_rescale
        elif hA_rescale == hB_rescale:
            hD_rescale = hC_rescale
        else:
            hD_rescale = bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = hOuterD * hD_rescale

        innerD = Rectangle.fromCenter(Point(xD, yD), wD, hD)

        return BiRectangle(outerD, innerD)

