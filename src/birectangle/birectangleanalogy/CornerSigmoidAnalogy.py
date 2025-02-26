from src.birectangle.birectangleanalogy.BiRectangleAnalogy import BiRectangleAnalogy
from src.birectangle.BiRectangle import BiRectangle
from src.basicanalogies.realnumbers import bounded
from src.birectangle.rectangleanalogy.TopLeftDimAnalogy import TopLeftDimAnalogy
from src.birectangle.Rectangle import Rectangle
from src.birectangle.Point import Point


# TODO: documentation
class CornerAnalogy(BiRectangleAnalogy):
    """
    Pierre-Alexandre analogy on bi-rectangles
    """
    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        if not outerRectD:
            outerRectD = TopLeftDimAnalogy().analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)

        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA.innerRectangle.x_min - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        xB_rescale = (BRB.innerRectangle.x_min - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        xC_rescale = (BRC.innerRectangle.x_min - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()
        xD_rescale = bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerRectD.x_min + outerRectD.width() * xD_rescale

        yA_rescale = (- BRA.innerRectangle.y_max + BRA.outerRectangle.y_max) / BRA.outerRectangle.height()
        yB_rescale = (- BRB.innerRectangle.y_max + BRB.outerRectangle.y_max) / BRB.outerRectangle.height()
        yC_rescale = (- BRC.innerRectangle.y_max + BRC.outerRectangle.y_max) / BRC.outerRectangle.height()
        yD_rescale = bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerRectD.y_max - outerRectD.height() * yD_rescale

        wA_rescale = (BRA.innerRectangle.width() + BRA.innerRectangle.x_min
                      - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        wB_rescale = (BRB.innerRectangle.width() + BRB.innerRectangle.x_min
                      - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        wC_rescale = (BRC.innerRectangle.width() + BRC.innerRectangle.x_min
                      - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()

        # if-elif added
        wD_rescale = bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = outerRectD.x_min - xD + outerRectD.width() * wD_rescale

        hA_rescale = (BRA.innerRectangle.height() - BRA.innerRectangle.y_max
                      + BRA.outerRectangle.y_max) / BRA.outerRectangle.height()
        hB_rescale = (BRB.innerRectangle.height() - BRB.innerRectangle.y_max
                      + BRB.outerRectangle.y_max) / BRB.outerRectangle.height()
        hC_rescale = (BRC.innerRectangle.height() - BRC.innerRectangle.y_max
                      + BRC.outerRectangle.y_max) / BRC.outerRectangle.height()

        # if-elif added
        hD_rescale = bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = yD - outerRectD.y_max + outerRectD.height() * hD_rescale

        innerD = Rectangle.fromTopLeft(Point(xD, yD), wD, hD)

        return BiRectangle(outerRectD, innerD)

