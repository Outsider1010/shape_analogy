from src.basicanalogies.realnumbers import asc_couple
from src.birectangle.bi_rectangle import BiRectangle
from src.birectangle.rectangle import Rectangle
from src.birectangle.birectangleanalogy.bi_rectangle_analogy import BiRectangleAnalogy
from src.birectangle.rectangleanalogy.center_dim_analogy import CenterDimAnalogy


class BiSegmentAnalogy(BiRectangleAnalogy):
    """
        Pierre-Alexandre bi-segment analogy on bi-rectangles
    """

    def __init__(self, rectangleAnalogy = CenterDimAnalogy()):
        self.rectAnalogy = rectangleAnalogy

    def analogy(self, BRA: BiRectangle, BRB: BiRectangle, BRC: BiRectangle, outerRectD: Rectangle | None = None) -> BiRectangle:
        if not outerRectD:
            outerRectD = self.rectAnalogy.analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        wOuterD = outerRectD.width()
        hOuterD = outerRectD.height()

        x_minA_rescale = (BRA.innerRectangle.x_min - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        x_minB_rescale = (BRB.innerRectangle.x_min - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        x_minC_rescale = (BRC.innerRectangle.x_min - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()

        x_maxA_rescale = (BRA.innerRectangle.x_max - BRA.outerRectangle.x_min) / BRA.outerRectangle.width()
        x_maxB_rescale = (BRB.innerRectangle.x_max - BRB.outerRectangle.x_min) / BRB.outerRectangle.width()
        x_maxC_rescale = (BRC.innerRectangle.x_max - BRC.outerRectangle.x_min) / BRC.outerRectangle.width()

        x_minD_rescale, x_maxD_rescale = asc_couple((x_minA_rescale, x_maxA_rescale),
                                                    (x_minB_rescale, x_maxB_rescale),
                                                    (x_minC_rescale, x_maxC_rescale))

        x_minD = outerRectD.x_min + x_minD_rescale * wOuterD
        x_maxD = outerRectD.x_min + x_maxD_rescale * wOuterD

        y_minA_rescale = (BRA.innerRectangle.y_min - BRA.outerRectangle.y_min) / BRA.outerRectangle.height()
        y_minB_rescale = (BRB.innerRectangle.y_min - BRB.outerRectangle.y_min) / BRB.outerRectangle.height()
        y_minC_rescale = (BRC.innerRectangle.y_min - BRC.outerRectangle.y_min) / BRC.outerRectangle.height()

        y_maxA_rescale = (BRA.innerRectangle.y_max - BRA.outerRectangle.y_min) / BRA.outerRectangle.height()
        y_maxB_rescale = (BRB.innerRectangle.y_max - BRB.outerRectangle.y_min) / BRB.outerRectangle.height()
        y_maxC_rescale = (BRC.innerRectangle.y_max - BRC.outerRectangle.y_min) / BRC.outerRectangle.height()

        y_minD_rescale, y_maxD_rescale = asc_couple((y_minA_rescale, y_maxA_rescale),
                                                    (y_minB_rescale, y_maxB_rescale),
                                                    (y_minC_rescale, y_maxC_rescale))

        y_minD = outerRectD.y_min + y_minD_rescale * hOuterD
        y_maxD = outerRectD.y_min + y_maxD_rescale * hOuterD

        return BiRectangle(outerRectD, Rectangle(x_minD, x_maxD, y_minD, y_maxD))