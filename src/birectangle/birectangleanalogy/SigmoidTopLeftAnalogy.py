from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.basicanalogies.realnumbers import bounded
from src.birectangle.rectangleanalogy.TopLeftDimAnalogy import TopLeftDimAnalogy
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point


class SigmoidTopLeftAnalogy(BiRectangleAnalogy):
    """
    Pierre-Alexandre analogy on bi-rectangles
    """
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle) -> BiRectangle:
        outerD = TopLeftDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)

        BRA_inner_topLeft = BRA.innerRectangle.topLeft()
        BRA_outer_topLeft = BRA.outerRectangle.topLeft()
        BRB_inner_topLeft = BRB.innerRectangle.topLeft()
        BRB_outer_topLeft = BRB.outerRectangle.topLeft()
        BRC_inner_topLeft = BRC.innerRectangle.topLeft()
        BRC_outer_topLeft = BRC.outerRectangle.topLeft()
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA_inner_topLeft.x - BRA_outer_topLeft.x) / BRA.outerRectangle.width()
        xB_rescale = (BRB_inner_topLeft.x - BRB_outer_topLeft.x) / BRB.outerRectangle.width()
        xC_rescale = (BRC_inner_topLeft.x - BRC_outer_topLeft.x) / BRC.outerRectangle.width()
        xD_rescale = bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerD.x_min + outerD.width() * xD_rescale

        yA_rescale = (- BRA_inner_topLeft.y + BRA_outer_topLeft.y) / BRA.outerRectangle.height()
        yB_rescale = (- BRB_inner_topLeft.y + BRB_outer_topLeft.y) / BRB.outerRectangle.height()
        yC_rescale = (- BRC_inner_topLeft.y + BRC_outer_topLeft.y) / BRC.outerRectangle.height()
        yD_rescale = bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerD.y_max - outerD.height() * yD_rescale

        wA_rescale = (BRA.innerRectangle.width() + BRA_inner_topLeft.x
                      - BRA_outer_topLeft.x) / BRA.outerRectangle.width()
        wB_rescale = (BRB.innerRectangle.width() + BRB_inner_topLeft.x
                      - BRB_outer_topLeft.x) / BRB.outerRectangle.width()
        wC_rescale = (BRC.innerRectangle.width() + BRC_inner_topLeft.x
                      - BRC_outer_topLeft.x) / BRC.outerRectangle.width()

        # if-elif added
        if wA_rescale == wC_rescale == 1:
            wD_rescale = wB_rescale
        elif wA_rescale == wB_rescale == 1:
            wD_rescale = wC_rescale
        else:
            wD_rescale = bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = outerD.x_min - xD + outerD.width() * wD_rescale

        hA_rescale = (BRA.innerRectangle.height() - BRA_inner_topLeft.y
                      + BRA_outer_topLeft.y) / BRA.outerRectangle.height()
        hB_rescale = (BRB.innerRectangle.height() - BRB_inner_topLeft.y
                      + BRB_outer_topLeft.y) / BRB.outerRectangle.height()
        hC_rescale = (BRC.innerRectangle.height() - BRC_inner_topLeft.y
                      + BRC_outer_topLeft.y) / BRC.outerRectangle.height()

        # if-elif added
        if hA_rescale == hC_rescale == 1:
            hD_rescale = hB_rescale
        elif hA_rescale == hB_rescale == 1:
            hD_rescale = hC_rescale
        else:
            hD_rescale = bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = yD - outerD.y_max + outerD.height() * hD_rescale

        innerD = Rectangle.fromTopLeft(Point(xD, yD), wD, hD)

        return BiRectangle(outerD, innerD)

